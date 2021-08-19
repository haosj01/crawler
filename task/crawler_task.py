#!/usr/bin/python
# -*- coding: UTF-8 -*-

from setting.project_config import *
from service.golden_service import Golden
from service.coindesk_service import Coindesk


def crawler_jinse_task():
    if environment == "prod":
        try:
            logger.info("====开启爬虫定时任务,爬取金色快讯====")
            Golden.save_lives()
            logger.info("====爬取金色快讯结束=========")
        except Exception as e:
            logger.error("爬取金色快讯异常###{}",e)
    else:
        logger.info("====测试环境不执行爬虫=========")


def crawler_coindesk_task():
    if environment == "prod":
        try:
            logger.info("====开启爬虫定时任务,爬取coindesk资讯====")
            Coindesk.save_news()
            logger.info("====爬取coindesk资讯结束=========")
        except Exception as e:
            logger.error("爬取coindesk资讯###{}",e)
    else:
        logger.info("====测试环境不执行coindesk资讯=========")