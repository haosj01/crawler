#!/usr/bin/python
# -*- coding: UTF-8 -*-
from flask import Flask
from flask_apscheduler import APScheduler
from setting.project_config import *
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app, supports_credentials=True)
    from controller.xwcapi import xc
    from controller.xt_news_controller import ac
    from controller.coin_type_controller import ct
    app.register_blueprint(ac)
    app.register_blueprint(ct)
    app.register_blueprint(xc)
    app.config.from_object(APSchedulerJobConfig)
    # 初始化Flask-APScheduler，定时任务
    scheduler = APScheduler()
    scheduler.init_app(app)
    scheduler.start()
    logger.info("============start success=============")
    return app
