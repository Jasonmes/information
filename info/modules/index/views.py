#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Jason Mess

from . import index_bp
from flask import session, current_app


"""
使用蓝图对象
"""


@index_bp.route('/')
def hello_world():

    current_app.logger.debug("记录日志")
    """
    没有调整之前，数据存在flask后端服务器，只是将session_id使用cookie的方式给了客户端
    :return:
    """
    session["name"] = "curry"
    return "Hello World! 6666"
