#!/usr/bin/python
# -*- coding: UTF-8 -*-

from flask import request
from service.coin_price_service import Coin_price_service
from setting.project_config import *
from flask.json import jsonify
from flask import Blueprint
from service.xwcapi_service import *
import traceback
from dto.reslut_dto import Reslut_dto
import json
import requests

xc = Blueprint("xwcapi", __name__)


@xc.route("/service/xwcapi/mainCoinPrice", methods=["GET"])
def coinPrice():
    res = mainCoinPrice()
    return res


@xc.route("/service/xwcapi/getStatis", methods=["POST"])
def getStatis():
    res = getApiStatis()
    return res


@xc.route("/api/getDaiTransactionList", methods=["POST"])
def getDaiTransactionList():
    data = json.loads(request.get_data(as_text=True))
    res = getDaiTransactionListService(data)
    return res
