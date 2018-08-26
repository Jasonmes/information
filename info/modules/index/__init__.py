#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Jason Mess

"""
首页模块
"""
from flask import Blueprint

"""
创建蓝图对象
url_prefix="/index"
"""
index_bp = Blueprint("index", __name__)

"""
切记：让index模块知道有views.py这个文件
"""
from .views import *