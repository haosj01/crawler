#!/usr/bin/python
# -*- coding: UTF-8 -*-
from tools.connect_mysql import ConnectMySQL


class Coin_price(object):
    def __init__(self):
        self.db = ConnectMySQL()

    def get_coin_type(self):
        sql = r"SELECT `id`,`name` FROM coin_type"
        data = self.db.query_mysql(sql)
        return data

    def get_coin_price_by_name(self,name):
        sql = r"SELECT ct.`name`,cp.price_cny,cp.price_usd FROM coin_type ct " \
              r"LEFT JOIN coin_price cp on ct.id = cp.coin_id WHERE ct.`name` = '%s' limit 1"%name
        data = self.db.query_mysql(sql)
        return data

    def update_coin_price(self,coin_id,cny,usd):
        sql = r"UPDATE coin_price SET price_cny = '%s', price_usd = '%s' WHERE coin_id = '%s'"%(cny,usd,coin_id)
        self.db.update_mysql(sql)

    def save_coin_price(self,coin_id,cny,usd):
        sql = r"INSERT INTO `crawler_info`.`coin_price`(`coin_id`, `price_cny`, `price_usd`) " \
              r"VALUES ('%s', '%s', '%s')"%(coin_id,cny,usd)
        self.db.insert_mysql(sql)

    def get_count_coin_price(self,coin_id):
        sql = r"SELECT COUNT(coin_id) FROM coin_price WHERE coin_id = '%s'"%coin_id
        return self.db.query_mysql(sql)[0][0]


