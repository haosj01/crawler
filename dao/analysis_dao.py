#!/usr/bin/python
# -*- coding: UTF-8 -*-

from tools.connect_mysql import ConnectMySQL

db= ConnectMySQL()
def save(reactid,tittle,content):
    sql = r"INSERT INTO crawler_info(reactid, tittle, content, create_time) VALUES ('%s','%s','%s',DATE_FORMAT(NOW(),'%%Y-%%m-%%d %%H:%%i:%%S'))"%(reactid,tittle,content)
    db.insert_mysql(sql)

def find_page(start,size):
    sql = r"SELECT`id`,reactid,tittle,content,create_time FROM crawler_info ORDER BY create_time desc LIMIT %d,%d"%(start,size)
    results = db.query_mysql(sql)
    return results

def find_count():
    sql = r"SELECT COUNT(`id`) FROM crawler_info"
    total = db.query_mysql(sql)[0][0]
    return total
