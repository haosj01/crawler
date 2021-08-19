#!/usr/bin/python
# -*- coding: UTF-8 -*-
import traceback
from setting.project_config import *
import urllib3
from bs4 import BeautifulSoup
import requests
import json
import random
from helper.user_agents import USER_AGENTS


class HttpRequestUtil:
    def __init__(self):
        self.url = ''
        self.params = ''
        self.type = 'post'
        # 默认post请求
        self.header = {}
        # 默认请求头
        self.addheader = ''
        self.run_res = ''
        self.cookies = []

    def set_header(self, header):
        self.header.update(header)
        return self

    def update_header(self):
        header = random.choice(USER_AGENTS)
        self.set_header(header)
        return self

    def get_header(self):
        return self.header

    def http_main(self, url, method, data=None,timeout=40):
        global r
        urllib3.disable_warnings()
        if 'post' == str.lower(method):
            try:
                r = requests.post(url, verify=False, headers=self.header, data=json.dumps(data),timeout=timeout)
            except:
                logger.error('request exeception ==>{}',traceback.format_exc())
        if 'get' == str.lower(method):
            try:
                r = requests.get(url, verify=False, headers=self.header, params=data,timeout=timeout)
            except:
                logger.error('request exeception ==>{}',traceback.format_exc())
        r.encoding = 'UTF-8'
        # logger.debug("request response is{}", r.text)
        return r

    def get_main_json(self, url, data,timeout = 40):
        r = self.http_main(url, method="get", data=data,timeout=timeout)
        return r.json()

    def get_main_text(self, url, data):
        r = self.http_main(url, method="get", data=data)
        return r.text

    def post_main_json(self, url, data):
        r = self.http_main(url, method="post", data=data)
        return r.json()

    def get_main_soup(self, url, data=None):
        r = self.http_main(url, method="get",data=data)
        soup = BeautifulSoup(r.text, 'lxml')
        return soup

