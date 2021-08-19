#!/usr/bin/python
# -*- coding: UTF-8 -*-

from flask import request
from setting.project_config import *
from flask.json import jsonify
from flask import Blueprint
import traceback
from dto.reslut_dto import Reslut_dto
from service.xt_news_service import Xt_news
import json

ac = Blueprint("golden", __name__)


@ac.route('/golden/lives', methods=["GET"])
def golden_lives():
    logger.info("接口进来了========================")
    start_time = int(round(time.time() * 1000))
    num = request.args.get("pageNum", "")
    size = request.args.get("pageSize", "")
    category = request.args.get("category")
    lang = request.headers.get("App-Language")
    try:
        if num == "" or size == "" or int(num) < 1:
            res = Reslut_dto("1", None, "request parameter exeception")
            return jsonify(res)
        obj = Xt_news.find_jinse_lives(int(num), int(size), category, lang)
        json_obj = jsonify(obj)
        end_time = int(round(time.time() * 1000))
        t = end_time - start_time
        logger.info("=================lives接口消耗的时间{}", t)
        return json_obj
    except ValueError as e:
        logger.error(traceback.format_exc())
        res = Reslut_dto("1", None, "request parameter exeception")
        return jsonify(res)
    except Exception:
        logger.error("查询资讯接口异常：{}", traceback.format_exc())
        res = Reslut_dto("1", None, "request exeception")
        return jsonify(res)


@ac.route('/golden/zan', methods=["POST"])
def golden_zan():
    try:
        data = json.loads(request.get_data(as_text=True))
        gid = data["id"]
        gtype = data["type"]
        lang = request.headers.get("App-Language")
        obj = Xt_news.golden_zan(gid, gtype, lang)
        print(obj)
        return jsonify(obj)
    except Exception:
        logger.error("点赞接口异常：{}", traceback.format_exc())
        res = Reslut_dto("1", None, "request exeception")
        end_time = int(round(time.time() * 1000))
        return jsonify(res)


@ac.route('/golden/live', methods=["GET"])
def find_live_id():
    try:
        lid = request.args.get("id")
        lang = request.headers.get("App-Language")
        obj = Xt_news.find_live_id(lid, lang)
        return obj
    except IndexError:
        return jsonify({"code": "0", "data": {}, "msg": "success"})
    except Exception:
        logger.error("查询资讯信息接口异常：{}", traceback.format_exc())
        return jsonify({"code": "1", "data": {}, "msg": "request exeception"})
