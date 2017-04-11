# import requests
# from bs4 import BeautifulSoup
import os
import pickle
from selenium import webdriver
import time
import psycopg2
from bs4 import BeautifulSoup
import re
from psql import *
from utils import *
from settings import *
import requests
import json
from os import listdir
from os.path import isfile, join
# from seleniumrequests import Chrome
# from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
'''
python

refresh('cb')

from cb import *

w = getc()

InsertPage(w):

Run(wd, 2)

w = getWebDriver()

w.get("https://httpbin.org/get?show_env=1")

req = getRequests(w)

req = getRequests()


r = req.get('http://httpbin.org/headers')

r = req.get('https://httpbin.org/get?show_env=1')

r.json()

sss = json.dumps(o["Results"])

'''

'''
def getApiResult(wd):
    return wd.execute_script("return ...")

def getRaw(result):
    list = [result['Id'],result['OtherNumber'],json.dumps(result)]
    return tuple(list)

def InsertRaw(elements):
    schema = 'INSERT INTO raw (id, other_number, raw) VALUES (%s, %s, %s)'
    PExec(dsn_raw,schema,GetElementssArray(elements, getRaw))    
'''
def InsertPage(wd):
    o = getApiResult(wd)
    InsertRaw(o["Results"])    
    InsertId(o["Results"])
    return o

'''
def getNextButton(w):
    return w.find_element_by_id('...')
'''
def Run(wd, pages=None):
    o = InsertPage(wd)
    pageNum = pages if pages else LogExp(getPageNum,o)
    for num in range(2,pageNum):
        time.sleep(3)
        dd = LogExp(getNextButton,wd)
        dd.click()
        InsertPage(wd)

'''
def InitApISource(browser):
    url = "https://httpbin.org/get?show_env=1"
    browser.get(url)
    browser.implicitly_wait(10)
    html = browser.page_source

    writeFile("00.html",html.encode('utf-8'),"wb")
    
    content = browser.find_element_by_css_selector('div.class_div')
    dd = content.find_element_by_css_selector('div.class_btn')
    dd.click()

    return browser
'''
def getc():
    time.sleep(2)
    browser = getWebDriver()
    InitApISource(browser)

'''
#payload = {"latitude1":43.78760887990924,"longitude1":-79.4278062438965,"latitude2":43.81238855081077,"longitude2":-79.33210502624513}
r = getSold(43.78760887990924,43.81238855081077,-79.4278062438965,-79.33210502624513)
print(r)
'''
def getSold(url,latitude1,latitude2,longitude1,longitude2):
    time.sleep(1)
    payload = {"latitude1":latitude1,"longitude1":longitude1,"latitude2":latitude2,"longitude2":longitude2}
    req = getRequests()
    # r = requests.post(url, data=json.dumps(payload))
    r = req.post(url, data=json.dumps(payload))
    log('{0},{1},{2},{3}'.format(latitude1,latitude2,longitude1,longitude2))
    return r

LongitudeMin = -128.02981853485105
LongitudeMax = -60.67631874511719
LatitudeMin = 20.9452976572409
LatitudeMax = 60.3041267770092
StepLa = 0.0507796709015304
StepLo = 0.0957012176513672

'''
getSoldtoFile(43.78760887990924,43.81238855081077,-79.4278062438965,-79.33210502624513,'tmp/20170406/0_0.json')
'''
def getSoldtoFile(url,latitude1,latitude2,longitude1,longitude2,file):
    try:
        if not isFileExists(file):
            r = getSold(url,latitude1,latitude2,longitude1,longitude2)
            dumpJson(file,r.json())
            log(file)
    except Exception as e: 
        log(str(e))

def getSoldEdge(url,latitude1, latitude2, longitude1, longitude2, folder):
    getSoldtoFile(url,latitude2, LatitudeMax, LongitudeMin, LongitudeMax, join(folder,'north.json'))
    getSoldtoFile(url,LatitudeMin, latitude1, LongitudeMin, LongitudeMax, join(folder,'south.json'))
    getSoldtoFile(url,LatitudeMin, LatitudeMax, longitude2, LongitudeMax, join(folder,'east.json'))
    getSoldtoFile(url,LatitudeMin, LatitudeMax, LongitudeMin, longitude1, join(folder,'west.json'))


def getSoldInside(url,latitude1,latitude2,longitude1,longitude2,stepla,steplo,folder):
    listla = getList(latitude1, latitude2 , stepla)
    listlo = getList(longitude1, longitude2 , steplo)
    for n in range(0, len(listla)-1):
        for m in range(0, len(listlo)-1):
            getSoldtoFile(url,listla[n],listla[n+1],listlo[m],listlo[m+1],join(folder,'{0}_{1}.json'.format(n,m)))
            
def RunGetSold(name, url):
    latitude1 = 43.3041267770092
    latitude2 = 44.41611706762943
    longitude1 = -80.67631874511719
    longitude2 = -78.48591957519531
    folder = getStrFromDate()
    folder = join('tmp',folder,name)
    getSoldEdge(url,latitude1,latitude2,longitude1,longitude2,folder)
    getSoldInside(url,latitude1,latitude2,longitude1,longitude2,StepLa,StepLo,folder)

'''
RunGetSolds(dict_sold)
'''
def RunGetSolds(d):
    for name,url in d.items():
        RunGetSold(name, url)