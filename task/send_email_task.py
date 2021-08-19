#!/usr/bin/python
# -*- coding: UTF-8 -*-

import smtplib
from email.mime.text import MIMEText
from email.header import Header
from setting.email_config import email_config
from setting.project_config import *
from service.constellation_service import Constellation
import traceback
import time


def send_email():
    global server, html
    username = email_config["username"]
    password = email_config["password"]
    receivers = email_config["toEmail"]
    host = email_config["host"]
    logger.info("开始发送邮件")
    const = Constellation()
    constellation = const.constellation()
    table = ""
    if not constellation:
        table = """
        <tr>
            <td style="padding:0 10px">无</td>
            <td style="padding:0 10px">0</td>
            <td style="padding:0 10px">0</td>
            <td style="padding:0 10px">0</td>
            <td style="padding:0 10px">0</td>
            <td style="padding:0 10px">0</td>
            <td style="padding:0 10px">0</td>
            <td style="padding:0 10px">0</td>
        </tr>
        """
    else:
        for var in constellation:
            recommender = constellation[var]["recommender"]
            usdt_order = constellation[var]["usdt_order"]
            usdt_recharge = constellation[var]["usdt_recharge"]
            usdt_people = constellation[var]["usdt_people"]
            sxc_ordere = constellation[var]["sxc_order"]
            sxc_people = constellation[var]["sxc_people"]
            sxc_recharge = constellation[var]["sxc_recharge"]
            html = f"""
                <tr>
                    <td style="padding:0 10px">{var}</td>
                    <td style="padding:0 10px">{recommender}</td>
                    <td style="padding:0 10px">{usdt_order}</td>
                    <td style="padding:0 10px">{usdt_people}</td>
                    <td style="padding:0 10px">{usdt_recharge}</td>
                    <td style="padding:0 10px">{sxc_ordere}</td>
                    <td style="padding:0 10px">{sxc_people}</td>
                    <td style="padding:0 10px">{sxc_recharge}</td>
                </tr>
            """
            table += html

    total_info = const.total_info()
    tolal_people = total_info[0]
    tolal_usdt = total_info[1]
    tolal_sxc = total_info[2]
    mail_msg = f"""
    <table border="1"  cellspacing="0">
     <tr>
        <th style="color:red;padding:0 10px">归属地</th>
        <th style="color:red;padding:0 10px">邀请注册</th>
        <th style="color:red;padding:0 10px">购买金额(USDT)</th>
        <th style="color:red;padding:0 10px">购买人数(USDT)</th>
        <th style="color:red;padding:0 10px">充值金额(USDT)</th>
        <th style="color:red;padding:0 10px">购买金额(SXC)</th>
        <th style="color:red;padding:0 10px">购买人数(SXC)</th>
        <th style="color:red;padding:0 10px">充值金额(SXC)</th>
    </tr>
    {table}
    </table>
    <br>
        <table border="1"  cellspacing="0">
        <tr>
            <th style="color:red;padding:0 10px">累计购买人数</th>
            <th style="color:red;padding:0 10px">累计购买总金额(USDT)</th>
            <th style="color:red;padding:0 10px">累计购买总金额(SXC)</th>
        </tr>
        <tr>
            <td style="padding:0 10px">{tolal_people}</td>
            <td style="padding:0 10px">{tolal_usdt}</td>
            <td style="padding:0 10px">{tolal_sxc}</td>
        </tr>
    </table>
    """
    msg = MIMEText(mail_msg, 'html', 'utf-8')
    today = time.strftime("%Y-%m-%d", time.localtime())
    subject = f'星座云库{today}数据'
    msg['Subject'] = Header(subject, 'utf-8')
    try:
        server = smtplib.SMTP_SSL(host)
        server.login(username, password)
        server.sendmail(username, receivers, msg.as_string())
        logger.info("邮件发送成功")
    except smtplib.SMTPException:
        logger.error("Error: 无法发送邮件{}", traceback.format_exc())
    finally:
        server.quit()


def send_email_task():
    if environment == "prod":
        send_email()
    else:
        logger.info("====测试环境不执行发送邮件=========")

if __name__ == "__main__":
    send_email()
