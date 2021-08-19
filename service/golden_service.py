#!/usr/bin/python
# -*- coding: UTF-8 -*-
from tools.HttpRequestUtil import HttpRequestUtil
from setting.project_config import *
from dao import jinse_dao
import random
import re


class Golden(object):

    @classmethod
    def save_lives(cls):
        reqUtils = HttpRequestUtil()
        host = 'https://api.jinse.com/noah/v2/lives'
        # data = {
        #     "limit": "20",
        #     "reading": "false",
        #     "source": "web",
        #     "flag": "down",
        #     "id": "0",
        #     "category": ""
        # }
        data = {
            "limit": "20",
            "reading": "false",
            "flag": "down",
            "id": "0",
            "category": ""
        }
        reqUtils.update_header()
        for num in range(6):
            data["category"] = num
            # response = json.load(open(r"E:\json.txt", encoding='utf-8'))
            response = None
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
            except Exception:
                logger.error("解析json异常{},请求地址参数{}", response,data)
            time.sleep(random.randint(6, 12))

    @classmethod
    def filter_info(cls, info):
        pattern = r"【.*】"
        data = re.sub(pattern, '', info).replace("金色", "")
        return data

if __name__ == "__main__":
    Golden().save_lives()