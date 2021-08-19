#!/usr/bin/python
# -*- coding: UTF-8 -*-

from tools.HttpRequestUtil import HttpRequestUtil
from setting.project_config import *
from dao.coin_price_dao import Coin_price
import redis


class Coin_price_service(object):
    def __init__(self):
        self.reqUtils = HttpRequestUtil()
        self.price_dao = Coin_price()
        self.page = "coinPrice:"
        pool = redis.ConnectionPool(host=r_host, port=r_port, decode_responses=True, password=r_password)
        self.r = redis.Redis(connection_pool=pool)

    def get_cny_coin_price(self, coin_name):
        url = "https://www.xt.pub/exchange-main/api/web/1_0_0/getCoinPrice"
        data = {
            "coinName": coin_name
        }
        response = self.reqUtils.get_main_json(url, data,timeout=20)
        logger.info("请求getCoinPrice获取币价结果{}，币种类型{}", response, coin_name)
        price = response.get("info", "0.0000")
        return str(price)

    def get_usd_coin_price(self, coin_name):
        url = "https://api.xt.pub/data/api/v1/getTicker"
        if coin_name == "usdt":
            return "1"
        coin_name += "_usdt"
        data = {
            "market": coin_name
        }
        response = self.reqUtils.get_main_json(url, data,timeout=20)
        logger.info("请求getTicker获取币价结果{}，币种类型{}", response, coin_name)
        price = response.get("price", "0.0000")
        return str(price)

    def save_price_redis(self):
        coin_types = self.price_dao.get_coin_type()
        for coin in coin_types:
            name = coin[1]
            self.save_redis(name)

    def get_redis(self, coin_name):
        rname = self.page + coin_name
        var = self.r.hgetall(rname)
        return var

    def save_redis(self, coin_name):
        rname = self.page + coin_name
        cny_price = self.get_cny_coin_price(coin_name)
        usd_price = self.get_usd_coin_price(coin_name)
        self.r.hset(rname, "cny_price", cny_price)
        self.r.hset(rname, "usd_price", usd_price)
        self.r.expire(self.page[:-1], 60)
        price = {
            "cny_price": cny_price,
            "usd_price": usd_price
        }
        return price

    def get_coin_price(self, coin_list: list):
        obj = {}
        data = {}
        for coin_name in coin_list:
            price = self.get_redis(coin_name)
            if not price:
                price = self.save_redis(coin_name)
                logger.debug("redis存在,币种名称{}", coin_name)
            else:
                logger.debug("redis存在,币种名称{}", coin_name)
            data[coin_name] = price
        obj["code"] = "0"
        obj["data"] = data
        obj["msg"] = "success"
        return obj
