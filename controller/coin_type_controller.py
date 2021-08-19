#!/usr/bin/python
# -*- coding: UTF-8 -*-

from flask import request
from service.coin_price_service import Coin_price_service
from setting.project_config import *
from flask.json import jsonify
from flask import Blueprint
import traceback
from dto.reslut_dto import Reslut_dto
import json

ct = Blueprint("coin_type", __name__)


@ct.route("/coin/getCoinPrice", methods=["POST"])
def get_coin_price():
    cps = Coin_price_service()
    try:
        data = json.loads(request.get_data(as_text=True))
        coin_List = data["coinType"]
        obj = cps.get_coin_price(coin_List)
        return jsonify(obj)
    except Exception:
        logger.error("获取币价接口异常：{}", traceback.format_exc())
        res = Reslut_dto("1", None, "request exeception")
        return jsonify(res)