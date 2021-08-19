#!/usr/bin/python
# -*- coding: UTF-8 -*-

from tools.connect_mysql import ConnectMySQL
from exeception.data_exception import DatabaseIndexException
db = ConnectMySQL()


class Coindesk_dao(object):
    def __init__(self):
        self.db = ConnectMySQL()

    def save_coindesk(self, idxno, tittle, content, news_time, create_time):
        sql = "INSERT INTO `crawler_coindesk`(`idxno`, `tittle`, `content`, `news_time`, `create_time`)" \
              "VALUES ('%s', '%s', '%s', '%s','%s')" % (idxno, tittle, content, news_time, create_time)
        self.db.insert_mysql(sql)

    def find_page(self, start, size):
        sql = "SELECT `id`,tittle,content,news_time,DATE_FORMAT(create_time,'%%Y-%%m-%%d') as live_date,up_counts,down_counts " \
              "FROM crawler_coindesk ORDER BY news_time DESC LIMIT %s,%s" % (start, size)
        results = db.query_mysql(sql)
        return results

    def find_count(self):
        sql = r"SELECT COUNT(id) FROM crawler_coindesk"
        total = db.query_mysql(sql)[0][0]
        return total

    def find_live_id(self, live_id):
        sql = "SELECT `id`,tittle,content,news_time,up_counts,down_counts FROM crawler_coindesk WHERE `id` = '%s' LIMIT 1" % live_id
        result = db.query_mysql(sql)
        return result[0]

    def find_live_idxno(self,idxno):
        sql = r"SELECT COUNT(id) FROM crawler_coindesk where idxno = %s"%idxno
        total = db.query_mysql(sql)[0][0]
        return total

    def query_zan(self,live_id):
        sql = r"select up_counts,down_counts FROM crawler_coindesk WHERE `id` = '%s'" % live_id
        result = db.query_mysql(sql)
        return result[0]

    def update_zan(self,live_id, live_type):
        type_counts = ""
        if "up" == live_type:
            type_counts = 'up_counts = up_counts'
        if "down" == live_type:
            type_counts = 'down_counts = down_counts'
        sql = r"UPDATE crawler_coindesk SET %s + 1 WHERE `id` = %s LIMIT 1" % (type_counts, live_id)
        db.update_mysql(sql)