import os
import os.path
import imp
import datetime
import json
import ast
from os import listdir
from os.path import isfile, join
import pickle
from selenium import webdriver
import time
import psycopg2
from bs4 import BeautifulSoup
import re
import requests
'''
import utils
imp.reload(utils)

refresh('utils')
from utils import *
'''

'''

'''
def RunDict(function, d, *arg):
    for key,value in d.items():
        function(name, url, *arg)

def isFileExists(file):
    return os.path.isfile(file)

'''
a = getFiles('tmp/20170406')
a = getFiles('tmp/20170406','.json')
'''
def getFiles(folder, ext=None):
    onlyfiles = [f for f in listdir(folder) if isfile(join(folder, f)) and (ext is None or os.path.splitext(f)[1] == ext) ]
    return onlyfiles

'''
runFolder(lambda x:print(x), './')
'''
def runFolder(function, folder, ext=None, *args, **kw):
    files = getFiles(folder,ext)
    for f in files:
        fromFile = join(folder,f)
        log(fromFile)
        LogExp(function, fromFile, *args, **kw)    

'''
g = lambda:1/0
LogExp(g)
LogExp(lambda:1/0)
LogExp((lambda x,y:x/y),4,2)
LogExp(tuple,[4,2])
'''
def LogExp(function, *args, **kw):
    try:
        a = function(*args, **kw)
    except Exception as e: 
        log(str(function))
        log(str(e)) 
        return None
    else:
        return a   
'''
s = readFile('20170406/21_15.json',byFileType=False)
'''
def readFile(file, default='', byFileType=True):
    data = default
    if not isFileExists(file):
        return data
    with open(file, 'r') as f:
        if byFileType:
            extension = os.path.splitext(file)[1]
            if extension == '.json':
                data = json.load(f)
            else:
                data=f.read()
        else:
            data=f.read()
#           data=myfile.read().replace('\n', '')
    return data

'''
d = readJson('tmp/20170407/west.json')
'''
def readJson(file, default=[]):
    return readFile(file,default)


'''
b = getJsonFromFile('20170406/21_15.json')
print(b)
s1 = '{{\'fruits\':{0}}}'.format(s)
b = json.loads(s1)
'''
def replaceJson(s):
    return s.replace('{\'', '{"').replace('\': \'','": "').replace('\':\'','":"').replace('\', \'','", "').replace('\',\'','","').replace('\':','":').replace('\'}','"}')

def getJsonFromFile(file):
    s = readFile(file,'[]',False)
    s = ast.literal_eval(s)
    return json.loads(replaceJson(str(s)))
'''
    data = json.loads('[]')
    if not isFileExists(file):
        return data
    with open(file) as data_file:
        data = json.load(data_file)
    return data
'''
'''
dumpJson('aaa.json',o["Results"])
'''
def dumpJson(filename, obj):
    try:
        writeFile(filename, obj, 'w')
    except Exception as e: 
        log(str(e))

'''
convertFiles('20170406','20170406real',convertToRealJson,'.json')
'''
def convertFiles(folderFrom, folderTo, function, ext=None):
    files = getFiles(folderFrom,ext)
    for f in files:
        fromFile = join(folderFrom,f)
        toFile = join(folderTo,f)
        try:
            function(fromFile, toFile)
            log('converted {0} to {1}'.format(fromFile,toFile))
        except Exception as e:
            log('error {0} to {1}'.format(fromFile,toFile)) 
            log(str(e))
           
'''
convertToRealJson('20170406/21_15.json','real/21_15.json')
convertToRealJson(join('20170406','21_15.json'),join('real','21_15.json'))
'''
def convertToRealJson(fileFrom, fileTo):
    b = getJsonFromFile(fileFrom)
    dumpJson(fileTo,b)
'''
writeFile('r.js',s,'w')
writeFile("00.html",html.encode('utf-8'),"wb")
writeFile('s.json',str(r.json()),'w')

   with open("00.html", "wb") as f:
        f.write(html.encode('utf-8'))
'''
def writeFile(filename, obj, format):
    d = os.path.dirname(filename)
    if d != '':
        os.makedirs(d, exist_ok=True)
    with open(filename, format) as f:
        if inType(obj, [str, bytes]):
            f.write(obj)
        else:
            json.dump(obj, f)

def inType(obj, typeList):
    result = False
    for t in typeList:
        if type(obj) is t:
            result = True
    return result

def log(s, file='log/log.txt'):
    writeFile(file, '{0} - {1}\n'.format(s,getStrFromDate(format='%Y-%m-%d %H:%M:%S')), 'a')
    print(s)

def getStrFromDate(date = datetime.datetime.now(), format='%Y%m%d'):
    return date.strftime(format)

def refresh(file, func = None):
    exec('import imp')
    exec('import {0}'.format(file))
    exec('imp.reload({0})'.format(file))
'''    if func is not None:
        exec('from {0} import {1}'.format(file, func))
    #exec 'import {0}'.format(s) in globals(), locals()
    exec('import imp'.format(s), globals(), locals())
    exec('import {0}'.format(s), globals(), locals())
    exec('imp.reload({0})'.format(s), globals(), locals())
    exec('from {0} import *'.format(s), globals(), locals())
    #exec()

    #from s import *'''

def l():
    print('*********************************************************')

def p(s):
    print(s)
    print('*****************************')

def getText(element, attr = None):
    if element != None:
        try:
            if (attr == None):
                return element.text
            else:
                return element[attr]
        except Exception as e: 
            print(str(e))
            return ''
    else:
        return ''

def isNone(value, default):
    if (value is None):
        return default
    else:
        return value

def getGen(min, max , step):
    yield(min)
    while min + step < max:
        min = min + step
        yield(min)
    yield(max)

def getList(min, max , step):
    return getListFromGen(getGen(min, max , step))

def getListFromGen(gen):
    l = []
    for i in gen:
        l.append(i)
    return l

'''
dd = {d[0][str(n)] for n in range(1,16)}
a = getListFromDict(d[0], sold_fields.split(','))
'''
def getListFromDict(d, names):
    l = {d[str(n)] for n in names}
    return l


'''
dw = {n:d[0][str(n)] for n in range(1,16)}
a = (lambda x,y:x[y])(d[0],'mlsno')
(lambda x,y:print(x[y]))(d[0],'mlsno')
GetElementssArray(d,(lambda x,y:print(x[y])),'mlsno')
GetElementssArray(d,(lambda x,y:x[y]),'mlsno')
'''
def GetElementssArray(elements, rowfunction, *args, **kw):
    a = []
    for e in elements:
        h = LogExp(rowfunction, e, *args, **kw)
        if h != None:
            a.append(h)

    return a

def getRequests(wd = None, reqHeader = None):
    # headers = reqHeader
    s = requests.session()
    s.proxies = {'http':  'socks5://127.0.0.1:9150',
                    'https': 'socks5://127.0.0.1:9150'}


    if reqHeader is not None:
        s.headers.update(reqHeader)
        
    if wd is not None:
        for cookie in wd.get_cookies():
            c = {cookie['name']: cookie['value']}
            s.cookies.update(c)
    return s

def getWebDriver():
    options = webdriver.ChromeOptions()
    # 设置中文
    options.add_argument('lang=en_US.UTF-8')
    # 更换头部
    options.add_argument('user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"')
    options.add_argument('--proxy-server=socks5://localhost:9150')
    # service_args = [ '--proxy=localhost:9150', '--proxy-type=socks5', ]
    browser = webdriver.Chrome(chrome_options=options)
    return browser