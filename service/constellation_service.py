#!/usr/bin/python
# -*- coding: UTF-8 -*-

from dao import constellation_dao


class Constellation(object):

    def __init__(self):
        self.users = [
            ['18616826841', '老板'],
            ['07075866888', '老板'],
            ['15155312412', '老板'],
            ['17681189929', '合肥'],
            ['17730219646', '合肥'],
            ['18555156633', '合肥'],
            ['15395006356', '合肥'],
            ['15056225976', '合肥'],
            ['18656355332', '合肥'],
            ['15075552670', '唐山'],
            ['13105158530', '上海'],
            ['17717587046', '上海'],
            ['18516300561', '上海'],
            ['17369082215', '成都'],
            ['18380471903', '成都'],
            ['18583256535', '成都'],
            ['13655187682', '测试账号']
        ]

    def set_users(self, users):
        self.users = users

    def find_recommender(self, phone):
        global attribution
        attribution = []
        for user in self.users:
            if (user[0] == phone):
                attribution.append(user[0])
                attribution.append(user[1])
                return attribution
        recommender_phones = constellation_dao.find_recommender(phone)
        if not recommender_phones:
            return attribution
        recommender_phone = str(recommender_phones[0][0])
        self.find_recommender(recommender_phone)
        return attribution

    def order(self):
        now_order = constellation_dao.find_now_order()
        if not now_order:
            yield []
            return
        for order in now_order:
            recommender = self.find_recommender(order[0])
            yield recommender[1],order[1],order[2]
        return

    def recommender(self):
        now_recommender = constellation_dao.find_now_recommender()
        if not now_recommender:
            yield []
            return
        for user in now_recommender:
            recommender = self.find_recommender(user[0])
            yield recommender
        return

    def recharge(self):
        find_recharge = constellation_dao.find_now_recharge()
        if not find_recharge:
            yield []
            return
        for recharge in find_recharge:
            recommender = self.find_recommender(recharge[0])
            yield recommender[1],recharge[1],recharge[2]
        return

    def constellation(self):
        obj = {}
        info = {
            "recommender":"0",
            "usdt_order": "0",
            "usdt_people": "0",
            "sxc_order": "0",
            "sxc_people": "0",
            "usdt_recharge": "0",
            "sxc_recharge": "0"
        }
        for order in self.order():
            if not order:
                break
            attribution = order[0]
            if not obj.get(attribution,""):
                obj[attribution] = info.copy()
            obj[attribution]["usdt_order"] = str(int(obj[attribution]["usdt_order"]) + int(order[1]))
            usdt_count = 1 if int(order[1]) > 0 else 0
            obj[attribution]["usdt_people"] = str(int(obj[attribution]["usdt_people"]) + usdt_count)
            obj[attribution]["sxc_order"] = str(int(obj[attribution]["sxc_order"]) + int(order[2]))
            sxc_count = 1 if int(order[2]) > 0 else 0
            obj[attribution]["sxc_people"] = str(int(obj[attribution]["sxc_people"]) + sxc_count)
        for recharge in self.recharge():
            if not recharge:
                break
            attribution = recharge[0]
            if not obj.get(attribution,""):
                obj[attribution] = info.copy()
            obj[attribution]["usdt_recharge"] = str(int(obj[attribution]["usdt_recharge"]) + int(recharge[1]))
            obj[attribution]["sxc_recharge"] = str(int(obj[attribution]["sxc_recharge"]) + int(recharge[2]))
        for recommender in self.recommender():
            if not recommender:
                break
            attribution = recommender[1]
            if not obj.get(attribution,""):
                obj[attribution] = info.copy()
            obj[attribution]["recommender"] = str(int(obj[attribution]["recommender"]) + 1)
        return obj

    def total_info(self):
        total = constellation_dao.total_info()
        return total