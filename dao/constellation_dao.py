#!/usr/bin/python
# -*- coding: UTF-8 -*-
from tools.connect_mysql import ConnectMySQL

db= ConnectMySQL()

def find_now_recommender():
    sql = "SELECT recommender_user_phone FROM `cybermoney_bz`.user_recommender WHERE create_time >= DATE_SUB( CURDATE(), INTERVAL 1 DAY ) AND create_time < CURDATE()"
    recommender_phones = db.query_mysql(sql)
    return recommender_phones

def find_now_recharge():
    sql = """
        SELECT 
            u.phone,
            SUM(IF(coin_type = 'usdt',balance_change,'0')),
            SUM(IF(coin_type = 'sxc',balance_change,'0'))
        FROM
        `cybermoney_bz`.wallet_flow w
         LEFT JOIN `cybermoney_bz`.`user` u ON w.user_id = u.id
        WHERE
           (w.operate_type = 'CZ' 
            OR (
            w.operate_type = 'XZ' 
            AND w.coin_type = 'SXC'))
            AND w.create_time >= DATE_SUB( CURDATE(), INTERVAL 1 DAY ) AND w.create_time < CURDATE() GROUP BY u.phone
    """
    recommender_phones = db.query_mysql(sql)
    return recommender_phones

def find_now_order():
    sql = "SELECT DISTINCT u.phone,sum(IF(r.coin_type = 'USDT', total_share_value, '0' )),sum(IF( r.coin_type = 'SXC', total_share_value, '0' )) FROM " \
          "`cybermoney_bz`.bz_financial_order r LEFT JOIN `cybermoney_bz`.`user` u ON r.user_id = u.id WHERE r.create_time >= DATE_SUB( CURDATE(), INTERVAL 1 DAY ) " \
          "AND r.create_time < CURDATE() GROUP BY u.phone"
    recommender_phones = db.query_mysql(sql)
    return recommender_phones

def find_recommender(phone):
    sql = r"select recommender_phone from `cybermoney_bz`.user_recommender where recommender_user_phone = '%s'"%(phone)
    recommender_phones = db.query_mysql(sql)
    return recommender_phones

def total_info():
    sql = "select COUNT(DISTINCT user_id),sum(IF(coin_type = 'USDT', total_share_value, '0' ))," \
          "sum(IF( coin_type = 'SXC', total_share_value, '0' )) from `cybermoney_bz`.bz_financial_order where create_time <  CURDATE() "
    recommender_phones = db.query_mysql(sql)
    return recommender_phones[0]


