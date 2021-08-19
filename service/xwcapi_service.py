#!/usr/bin/python
# -*- coding: UTF-8 -*-

import requests
import json
host = "https://explorer.whitecoin.info/api"


def mainCoinPrice():
    path = '/mainCoinPrice'
    url = host + path
    res = requests.get(url).json()
    return res


def getApiStatis():
    path = '/getStatis'
    url = host + path
    res = requests.post(url).json()
    return res


def getDaiTransactionListService(args):
    path = '/getDaiTransactionList'
    url = host + path
    header = {"Content-Type":"application/json"}
    res = requests.post(url,data=json.dumps(args),headers=header).json()
    return res