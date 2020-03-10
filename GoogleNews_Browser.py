#!/usr/bin/python
import re
import requests
import time
import unidecode
import pandas as pd
import mechanize
from itertools import chain
from mechanize import Browser
from mechanize import SelectControl
from mechanize import ListControl
from mechanize import HTMLForm
from mechanize import Control
from bs4 import BeautifulSoup
from time import gmtime, strftime

def browser_search(site, searchword):
    url = "https://news.google.com/search?q=" + str(searchword) + "&hl=en-US&gl=US&ceid=US%3Aen"
    br = Browser()
    br.set_handle_robots(False)
    br.addheaders = [('User-agent', 'Firefox')]

    br.open(url)
    br.select_form(nr=0)

    forms = [f for f in br.forms()]
    for control in forms[0].controls:
        print(control.name, control.type)

    ctl1 = br.form.find_control(type="text", nr=0)
    ctl1.clear()
    ctl1.disable = False
    print(br.form.find_control(type="text", nr=0))

    ctl2 = br.form.find_control(type="text", nr=1)
    ctl2.value = searchword
    print(br.form.find_control(type="text", nr=1))

    ctl3 = br.form.find_control(type="submitbutton")
    ctl3.readonly = False

    response = br.response()

    time.sleep(1)

    return response.read()

def get_news(resp):
    soup = BeautifulSoup(resp)
    #searchbox = soup.findAll("div", {"class": "SVJrMe"})

    article = soup.findAll("a", {"class": "DY5T1d"})
    publication = soup.findAll("a", {"class": "wEwyrc AVN2gc uQIVzc Sksgp"})
    number = [i for i in range(len(article))]
    news["Title"] = number

    counter = 0
    for tag in article:
        try:
            title = tag.string
            print("Recovering title: ", str(title))
            news.loc[counter, "Title"] = title
            counter += 1
        except:
            title = None
            print("No title was recovered")
            news.loc[counter, "Title"] = title
            counter += 1

    counter = 0
    for tag in publication:
        try:
            outlet = tag.string
            print("Recovering news outlet: ", outlet)
            news.loc[counter, "Outlet"] = outlet
        except:
            outlet = None
            print("No outlet was recovered")
            news.loc[counter, "Outlet"] = outlet

        try:
            times = tag.next_sibling.string
            print("Recovering time: ", times)
            news.loc[counter, "Date"] = times
            counter += 1
        except:
            times = None
            print("No time was recovered")
            news.loc[counter, "Date"] = times
            counter += 1

    for i in range(len(news["Date"])):
        if news.loc[i, "Date"] is not None:
            news.loc[i, "Recovered_Day"] = strftime('%Y-%m-%d')
            news.loc[i, "Recovered_Time"] = strftime("%H:%M:%S")
        elif news.loc[i, "Date"] is None:
            news.loc[i, "Recovered_Day"] = None
            news.loc[i, "Recovered_Time"] = None


response = browser_search(site="https://news.google.com/?hl=en-US&gl=US&ceid=US:en", searchword="Influenza")
news = pd.DataFrame()
get_news(resp=response)

news.to_csv("news_" + strftime('%Y-%m-%d') + ".csv", sep=",", encoding='utf-8', index=False)




