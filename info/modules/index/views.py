#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Jason Mess

from . import index_bp
from flask import session, current_app, render_template
from info import redis_store, models


@index_bp.route('/')
def index():

    """
    使用蓝图对象
    redis_store.set("name", "laowang")
    current_app.logger.debug("记录日志")
    没有调整之前，数据存在flask后端服务器，只是将session_id使用cookie的方式给了客户端
    :return:
    session["name"] = "curry"
    """
    print(current_app.url_map)
    return render_template("index.html")


@index_bp.route("/favicon.ico")
def favicon():
    """
    返回图标
    返回web头像图标
    :return:
    send_static_file:将static中的静态文件发送给浏览器
    """
    return current_app.send_static_file("news/favicon.ico")

