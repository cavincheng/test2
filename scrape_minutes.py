#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 15 11:42:23 2020

@author: notfunny6889
"""


import requests
#%%
#抓取網頁和解析HTML
from bs4 import BeautifulSoup
#%%
import re
##1996-2007 minutes html shape
#https://www.federalreserve.gov/fomc/minutes/20000202.htm  
## 2008 -
#https://www.federalreserve.gov/monetarypolicy/fomcminutes+date
#%%
def get_annual_minutes(y):
    page_link = requests.get('https://www.federalreserve.gov/monetarypolicy/fomchistorical{year}.htm'.format(year = y))
    #抓取網頁和解析HTML
    soup_link = BeautifulSoup(page_link.content, 'html.parser')
    #07年以前的link中herf的tag長相是/fomc/minutes/20070131.htm, [14:22]可以取得日期ex.20070131
    for link in soup_link.find_all('a'):
        if 1995<year <= 2007: 
            pattern = re.compile('/fomc/minutes/.*')
            if pattern.findall(link.get('href')) != []: 
                filename = pattern.findall(link.get('href'))[0][14:22]
        elif year<=1995:
            pattern = re.compile('/fomc/MINUTES/%d/.*'%year)
            if pattern.findall(link.get('href')) != []: 
                filename = pattern.findall(link.get('href'))[0][19:27]
        else:
        #07年以後的link中herf的tag長相是/monetarypolicy/fomcminutes20141217.htm, [27:35]可以取得日期ex.20141217
            pattern = re.compile('/monetarypolicy/fomcminutes.*')
            if pattern.findall(link.get('href')) != []: 
                filename = pattern.findall(link.get('href'))[0][27:35]
        #將page內的文字放入txt檔
        if pattern.findall(link.get('href')) != []:        
            page = requests.get("https://www.federalreserve.gov"+ pattern.findall(link.get('href'))[0])
            soup = BeautifulSoup(page.content, 'html.parser')
            txt = open("%s.txt"%filename,"w+",encoding="utf-8")
            for segment in range(len(soup.find_all('p'))):
                txt.write(soup.find_all('p')[segment].get_text())               
            txt.close()
#%%
year = 1992
for i in range(2015-year):
    year += i
    get_annual_minutes(year)
    year=1992
    

    