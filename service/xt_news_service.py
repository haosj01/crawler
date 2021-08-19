#!/usr/bin/python
# -*- coding: UTF-8 -*-

from setting.project_config import *
from dao import jinse_dao
import math
from service.cachekit import Cache
from dao.coindesk_dao import Coindesk_dao


class Xt_news(object):
    cache = Cache()
    coindesk_dao = Coindesk_dao()

    @staticmethod
    @cache.cached(timeout=60 * 10, key_prefix="xt_news")
    def find_jinse_lives(num, size, category, lang):
        obj = {}
        data = {}
        start = size * (num - 1)
        if "cn" == lang:
            data_info = jinse_dao.find_page(start, size, category)
            total = jinse_dao.find_count(category)
        elif "ko" == lang:
            data_info = Xt_news.coindesk_dao.find_page(start, size)
            total = Xt_news.coindesk_dao.find_count()
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
    def golden_zan(cls,gid,gtype,lang):
        obj = {}
        data = {}
        if "cn" == lang:
            jinse_dao.update_zan(gid, gtype)
            result = jinse_dao.query_zan(gid)
        elif "ko" == lang:
            cls.coindesk_dao.update_zan(gid, gtype)
            result = cls.coindesk_dao.query_zan(gid)
        else:
            result = [0, 0]
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

    @staticmethod
    @cache.cached(timeout=60 * 60 * 2, key_prefix="xt_news")
    def find_live_id(live_id, lang):
        if "cn" == lang:
            result = jinse_dao.find_live_id(live_id)
        elif "ko" == lang:
            result = Xt_news.coindesk_dao.find_live_id(live_id)
        else:
            result = jinse_dao.find_live_id_en(live_id)
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
