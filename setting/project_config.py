#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import time
import sys
from loguru import logger

parameter = sys.argv[1]
environment = os.getenv("measured_environment", parameter)
os.environ['TZ'] = 'Asia/Shanghai'

if environment == "test":
    # 测试环境
    # MySQL数据库配置
    a_d = '1'
    db_host = '192.168.110.11'
    db_port = 3306
    db_user = 'root'
    db_password = 'aWY4&B1Y@jr&Oy'
    db_database = 'crawler_info'

    r_host = '192.168.110.11'
    r_port = 6379
    r_password = ""
if environment == "prod":
    # 生成环境
    # MySQL数据库配置
    a_d = '2'
    db_host = '127.0.0.1'
    db_port = 6297
    db_user = 'root'
    db_password = 'Q#DYPXnjeTDKi2'
    db_database = 'crawler_info'

    r_host = 'localhost'
    r_port = 6379
    r_password = "bzvipcc"

if environment == "dev":
    # 生成环境
    # MySQL数据库配置
    a_d = '3'
    # db_host = '127.0.0.1'
    db_host = '154.209.69.116'
    db_port = 6297
    db_user = 'root'
    db_password = 'Q#DYPXnjeTDKi2'
    db_database = 'crawler_info'

    r_host = 'localhost'
    r_port = 6379
    r_password = "bzvipcc"

# 年月日
today = time.strftime("%Y-%m-%d", time.localtime())
# 获取日志地址
log_path = os.path.join(os.path.abspath(os.path.join(os.getcwd(), "../")), "logs")
if os.path.exists(log_path):
    pass
else:
    os.mkdir(log_path, mode=0o777)

# loguru日志配置
logger.add(
    f"{log_path}/api.log",
    format="{time:YYYY-MM-DD HH:mm:ss}|{level}|{message}",
    level="INFO",
    rotation="00:00",
    encoding="utf-8",
)


# 定时任务
class APSchedulerJobConfig(object):
    SCHEDULER_API_ENABLED = True
    SCHEDULER_TIMEZONE = 'Asia/Shanghai'
    JOBS = [
        {
            'id': '1',  # 任务唯一ID
            'func': 'task.send_email_task:send_email_task',
            'args': '',  # 如果function需要参数，就在这里添加
            'trigger': {
                "type": "cron",  # 类型
                # "day_of_week": "0-6", # 可定义具体哪几天要执行
                "hour": "8", # 小时数
                "minute": "10",
                # "second": "3"  # "*/3" 表示每3秒执行一次，单独一个"3" 表示每分钟的3秒。现在就是每一分钟的第3秒时循环执行。
            }
        },
        {
            'id': '2',  # 任务唯一ID
            'func': 'task.crawler_task:crawler_jinse_task',
            'args': '',  # 如果function需要参数，就在这里添加
            'trigger': 'interval',  # 指定任务触发器 interval
            # 'hours': 1
            'minutes': 20
        },
        {
            'id': '3',  # 任务唯一ID
            'func': 'task.coin_price_task:coin_price_task',
            'args': '',  # 如果function需要参数，就在这里添加
            'trigger': 'interval',  # 指定任务触发器 interval
            'minutes': 2
        },
        {
            'id': '4',  # 任务唯一ID
            'func': 'task.crawler_task:crawler_coindesk_task',
            'args': '',  # 如果function需要参数，就在这里添加
            'trigger': 'interval',  # 指定任务触发器 interval
            # 'hours': 1
            'minutes': 40
        }
    ]
