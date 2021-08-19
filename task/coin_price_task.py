#!/usr/bin/python
# -*- coding: UTF-8 -*-


from setting.project_config import *
from service.coin_price_service import Coin_price_service


def coin_price_task():
    if environment == "prod":
        try:
            logger.info("====开启定时任务,获取币价====")
            cps = Coin_price_service()
            cps.save_price_redis()
            logger.info("====获取币价结束=========")
        except Exception as e:
            logger.error("====获取币价异常========={}",e)
    else:
        logger.info("====测试环境不执行获取币价=========")