#!/usr/bin/python
# -*- coding: UTF-8 -*-
from tools.HttpRequestUtil import HttpRequestUtil
from setting.project_config import *
from dao import jinse_dao
import math
import time
import json
import re
import random
from service.cachekit import Cache


class Golden(object):
    cache = Cache()

    @classmethod
    def save_lives(cls):
        reqUtils = HttpRequestUtil()
        host = 'https://api.jinse.com/noah/v2/lives'
        data = {
            "limit": "20",
            "reading": "false",
            "source": "web",
            "flag": "down",
            "id": "0",
            "category": ""
        }
        # header = {
        #     "source": "web"
        # }
        headers = [
            {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'},
            {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0'},
            {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko'}
        ]
        reqUtils.set_header(headers[random.randint(0, 2)])
        for num in range(6):
            data["category"] = num
            # response = json.load(open(r"E:\json.txt", encoding='utf-8'))
            try:
                response = reqUtils.get_main_json(host, data)
                lives = response["list"][0]["lives"]
                lives.reverse()
                for live in lives:
                    live_id = live["id"]
                    if 1 == num or 2 == num or 4 == num:
                        count = jinse_dao.find_by_liveId(live_id)
                        if count > 0:
                            jinse_dao.update(live_id, num)
                            continue
                    content = cls.filter_info(live["content"])
                    tittle = live["content_prefix"]
                    created_at = live["created_at"]
                    format_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(created_at))
                    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                    format_data = time.strftime("%Y-%m-%d", time.localtime(created_at))
                    jinse_dao.save_live(live_id, tittle, content, format_time, current_time, format_data, num)
            except Exception as e:
                logger.error("解析json异常{}", e)
                raise e
            time.sleep(random.randint(6, 12))

    @classmethod
    @cache.cached(timeout=60 * 10, key_prefix="crawler_jinse")
    def find_jinse_lives(cls, num, size, category, lang):
        obj = {}
        data = {}
        start = size * (num - 1)
        if "cn" == lang:
            data_info = jinse_dao.find_page(start, size, category)
            total = jinse_dao.find_count(category)
        else:
            data_info = jinse_dao.find_page_en(start, size)
            total = jinse_dao.find_count_en()
        pages = math.ceil(total / size)
        obj["code"] = "0"
        data["current"] = num
        data["pages"] = pages
        data["size"] = size
        data["total"] = total
        records = []
        if data_info == None:
            data['records'] = records
            obj["data"] = data
            return obj
        date_set = set()
        for d in data_info:
            date = d[4]
            date_set.add(date)
        date_set = sorted(date_set)
        for var in date_set:
            record = {}
            record["date"] = var
            lisves = []
            for info in data_info:
                live_data = info[4]
                if var == live_data:
                    lisve = {}
                    lisve['id'] = info[0]
                    lisve['tittle'] = info[1]
                    lisve['content'] = info[2]
                    lisve['create_time'] = str(info[3])
                    lisve['up_counts'] = info[5]
                    lisve['down_counts'] = info[6]
                    diff = int(info[5]) - int(info[6])
                    if diff > 0:
                        zan_status = "up"
                    elif diff == 0:
                        zan_status = "normal"
                    else:
                        zan_status = "down"
                    lisve["zan_status"] = zan_status
                    lisves.append(lisve)
                else:
                    continue
            record["lives"] = lisves
            records.append(record)
        records.reverse()
        record_list = records.copy()
        data['records'] = record_list
        obj["data"] = data
        obj["msg"] = "success"
        return obj

    @classmethod
    def golden_zan(cls, id, type):
        jinse_dao.update_zan(id, type)
        result = jinse_dao.query_zan(id)
        obj = {}
        data = {}
        up_counts = result[0]
        down_counts = result[1]
        diff = int(up_counts) - int(down_counts)
        if diff > 0:
            zan_status = "up"
        elif diff == 0:
            zan_status = "normal"
        else:
            zan_status = "down"
        data["up_counts"] = up_counts
        data["down_counts"] = down_counts
        data["zan_status"] = zan_status
        obj["code"] = "0"
        obj["msg"] = "success"
        obj["data"] = data
        return obj

    @classmethod
    @cache.cached(timeout=60 * 60 * 2, key_prefix="crawler_jinse")
    def find_live_id(cls, id, lang):
        if "cn" == lang:
            result = jinse_dao.find_live_id(id)
        else:
            result = jinse_dao.find_live_id_en(id)
        obj = {}
        lisve = {}
        lisve['id'] = result[0]
        lisve['tittle'] = result[1]
        lisve['content'] = result[2]
        lisve['create_time'] = str(result[3])
        lisve['up_counts'] = result[4]
        lisve['down_counts'] = result[5]
        diff = int(result[4]) - int(result[5])
        if diff > 0:
            zan_status = "up"
        elif diff == 0:
            zan_status = "normal"
        else:
            zan_status = "down"
        lisve["zan_status"] = zan_status
        obj["code"] = "0"
        obj["msg"] = "success"
        obj["data"] = lisve
        return obj

    @classmethod
    def filter_info(cls, info):
        pattern = r"【.*】"
        data = re.sub(pattern, '', info).replace("金色", "")
        return data
