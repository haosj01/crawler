#!/usr/bin/python
# -*- coding: UTF-8 -*-

import requests
from bs4 import BeautifulSoup
from setting.project_config import *
from requests.packages import urllib3
from dao import analysis_dao
from lxml import etree
import math
import bs4
import re
import time
import json

host = 'https://www.aicoin.cn'

def getHTMLText(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
    }
    try:
        urllib3.disable_warnings()
        r = requests.get(url, verify=False,headers=headers)
        r.raise_for_status()
        r.encoding = 'UTF-8'
        soup = BeautifulSoup(r.text, 'lxml')
        return soup
    except:
        logger.error('http request exeception')

def save_info():
    request_url = host+"/news/market-analysis"
    soup = getHTMLText(request_url)
    list_soup = soup.select('h3 a')
    logger.info('爬取的数据===>{}', list_soup)
    list_soup.reverse()
    for info in list_soup:
        url_path = info.get('href')
        reactid = url_path.split('/')[-1].replace(".html","")
        textInfo = getHTMLText(host + url_path)
        content = filter_data(textInfo.section.text)
        tittle = textInfo.select('header h2')[0].text
        analysis_dao.save(reactid,tittle,content)
        time.sleep(20)

def filter_data(text):
    if ('更多优质分析解读请关注微信公众号' in text):
        pattern = '更多优质分析解读请关注微信公众号.*'
        data = re.sub(pattern, '', text)
    elif('热门资讯' in text):
        len = text.find('热门资讯')
        data = text[0:len]
    else:
        data = text
    return data

def find_analysis(num,size):
    obj = {}
    data = {}
    start = size *(num -1)
    data_info = analysis_dao.find_page(start,size)
    total = analysis_dao.find_count()
    pages = math.ceil(total/size)
    obj["code"] = "0"
    data ["current"] = num
    data["pages"] = pages
    data["size"] = size
    data["total"] = total
    data["msg"] = "success"
    records= []
    if data_info ==None:
        data['records'] = records
        obj["data"] = data
        return obj
    for info in data_info:
        record = {}
        record['id'] = info[0]
        record['tittle'] = info[2]
        record['content'] = info[3]
        record['create_time'] = str(info[4])
        records.append(record)
    data['records'] = records
    obj["data"] = data
    return obj

