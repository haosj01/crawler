#!/usr/bin/python
# -*- coding: UTF-8 -*-

from tools.connect_mysql import ConnectMySQL
from setting.project_config import *

db = ConnectMySQL()


def save_live(live_id, tittle, content, live_time, live_date, create_time, type):
    sql = r"INSERT INTO `crawler_golden`(`live_id`, `tittle`, `content`, `live_time`, `create_time`, `live_date`,  `type`) " \
          "VALUES ('%s', '%s', '%s', '%s', '%s','%s','%s')" \
          % (live_id, tittle, content, live_time, live_date, create_time, type)
    db.insert_mysql(sql)


def update(live_id, num):
    col = ""
    if "1" == str(num):
        col = "is_choice"
    if "2" == str(num):
        col = "is_data"
    if "4" == str(num):
        col = "is_notice"
    sql = r"UPDATE crawler_golden SET %s = 1 WHERE live_id = '%s'" % (col, live_id)
    db.update_mysql(sql)


def find_by_liveId(live_id):
    sql = r"SELECT COUNT(live_id) FROM crawler_golden WHERE live_id = '%s'" % live_id
    count = db.query_mysql(sql)[0][0]
    return count


def find_page(start, size, num):
    condition = ""
    num = str(num)
    if "0" == num:
        condition = r" in('0','1','2','4')"
    if "1" == num:
        condition = r" = '1' or is_choice = '1'"
    if "2" == num:
        condition = r" = '2' or is_data = '1'"
    if "3" == num:
        condition = r" ='3'"
    if "4" == num:
        condition = r" = '4' or is_notice = '1'"
    if "5" == num:
        condition = r" ='5'"
    sql = r"SELECT`id`,tittle,content,live_time,live_date,up_counts,down_counts FROM crawler_golden WHERE `" \
          "type` %s ORDER BY live_time desc LIMIT %s,%s" % (condition, start, size)
    results = db.query_mysql(sql)
    return results


def find_page_en(start, size):
    sql = r"SELECT id,article_title,content_str,create_time,DATE_FORMAT(create_time,'%%Y-%%m-%%d') " \
          r"as live_date,0,0 FROM `cybermoney_bz`.article WHERE type = '1' ORDER BY create_time DESC LIMIT %s,%s" % (
          start, size)
    results = db.query_mysql(sql)
    return results


def find_count_en():
    sql = r"SELECT COUNT(id) FROM `cybermoney_bz`.article WHERE type = '1'"
    total = db.query_mysql(sql)[0][0]
    return total


def find_count(num):
    condition = ""
    num = str(num)
    if "0" == num:
        condition = r" type in('0','1','2','4')"
    if "1" == num:
        condition = r" type = '1' or is_choice = '1'"
    if "2" == num:
        condition = r" type = '2' or is_data = '1'"
    if "3" == num:
        condition = r" type ='3'"
    if "4" == num:
        condition = r" type = '4' or is_notice = '1'"
    if "5" == num:
        condition = r" type ='5'"
    sql = r"SELECT COUNT(id) FROM crawler_golden where {}".format(condition)
    total = db.query_mysql(sql)[0][0]
    return total


def update_zan(live_id, live_type):
    type_counts = ""
    if "up" == live_type:
        type_counts = 'up_counts = up_counts'
    if "down" == live_type:
        type_counts = 'down_counts = down_counts'
    sql = r"UPDATE crawler_golden SET %s + 1 WHERE `id` = %s LIMIT 1" % (type_counts, live_id)
    db.update_mysql(sql)


def query_zan(live_id):
    sql = r"select up_counts,down_counts FROM crawler_golden  WHERE `id` = '%s'" % live_id
    result = db.query_mysql(sql)
    return result[0]


def find_live_id(live_id):
    sql = r"SELECT`id`,tittle,content,live_time,up_counts,down_counts FROM crawler_golden WHERE `id` = '%s' LIMIT 1" % live_id
    result = db.query_mysql(sql)
    return result[0]


def find_live_id_en(live_id):
    sql = r"SELECT id,article_title,content_str,create_time,0,0 FROM `cybermoney_bz`.article WHERE `id` = '%s' LIMIT 1" % live_id
    result = db.query_mysql(sql)
    return result[0]
