#!/usr/bin/python
# -*- coding: UTF-8 -*-
from tools.HttpRequestUtil import HttpRequestUtil
from setting.project_config import *
from dao.coindesk_dao import Coindesk_dao
import random
import datetime


class Coindesk():
    host = 'https://www.coindeskkorea.com/'
    reqUtils = HttpRequestUtil()
    coindesk_dao = Coindesk_dao()

    @classmethod
    def get_html_news(cls):
        cls.reqUtils.update_header()
        url = cls.host + "news/articleList.html"
        soup = cls.reqUtils.get_main_soup(url)
        return soup

    @classmethod
    def save_news(cls):
        soup = cls.get_html_news()
        list_soup = soup.select('div[class="list-titles table-cell"]  a')
        list_soup.reverse()
        for info in list_soup[1:]:
            try:
                logger.info("Coindesk info {}", info)
                href = info.get("href")
                tittle = info.text.replace("'", "\\'")
                idxno = href.split('=')[-1]
                if cls.is_idxno_exist(idxno):
                    text_info = cls.reqUtils.get_main_soup(cls.host + href)
                    content = text_info.select('div[id="article-view-content-div"]')[0].text
                    info_list = [cls.filter_info(x) for x in content.split("\n") if (x and x != "\xa0")]
                    news_time = cls.ko_time_transform(info_list[1])
                    logger.debug("news_time====={}", news_time)
                    news_list = info_list[3:info_list.index("Tag")]
                    news_content = "\n\n".join(news_list)
                    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                    cls.coindesk_dao.save_coindesk(idxno, tittle, news_content, news_time, current_time)
                else:
                    logger.info("Coindesk资讯已存在,idxno={}", idxno)
                    continue
            except Exception as e:
                logger.error("Coindesk资讯爬虫发生异常##{}", e)
            time.sleep(random.randint(8, 20))

    @classmethod
    def filter_info(cls, info) -> str:
        data = info.replace("\xa0", "").replace("'", "\\'")
        return data

    @classmethod
    def is_idxno_exist(cls, idxno) -> bool:
        res = cls.coindesk_dao.find_live_idxno(idxno)
        if res == 0:
            return True
        else:
            return False

    @classmethod
    def ko_time_transform(cls, tss1) -> str:
        time_array = time.strptime(tss1, "%Y년 %m월%d일 %H:%M")
        time_stamp = int(time.mktime(time_array))
        date_array = datetime.datetime.fromtimestamp(time_stamp)
        cn_time = date_array - datetime.timedelta(hours=1)
        transform_time = cn_time.strftime("%Y{y} %m{m}%d{d} %H:%M").format(y='년', m='월', d='일')
        return transform_time