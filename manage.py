#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Jason Mess

from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from redis import StrictRedis
from flask_wtf.csrf import CSRFProtect
from flask_session import Session


# 创建项目配置类
class Config(object):
    """
    项目配置类
    开启debug的模式
    """
    DEBUG = True

    """
    数据库链接配置
    并且不跟踪数据库修改
    """
    SQLALCHEMY_DATABASE_URI = "mysql://root:cq@127.0.0.1:3306/imformation16"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    """
    redis数据库配置信息
    REDIS_NUM : 第几个数据库
    """
    REDIS_HOST = "127.0.0.1"
    REDIS_PORT = 6379
    REDIS_NUM = 6

    """
    设置加密字符串
    
    import os
    os.urandom(48)
    import base64
    base64.b64encode(os.urandom(48))
    """
    SECRET_KEY = "EJxSi/538lWIb/Vk+ruFunGT/UHtGOzZ9sKwY15cuULGvfaGqisJaUf0/ZXmdwF7"

    """
    调整session存储位置 存储到redis
    指明session存储到那种类型的数据库
    """

    SESSION_REDIS = StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_NUM)
    """
    session需要数据加密
    设置不永久存储
    默认存储的有效时长
    """
    SESSION_USE_SIGNER = True
    SESSION_PERMANENT = False
    PERMANENT_SESSION_LIFETIME = 86400


app = Flask(__name__)
"""
2：注册配置信息到app对象
"""
app.config.from_object(Config)

"""
3：创建mysql数据库对象
"""
db = SQLAlchemy(app)

"""
4：创建redis数据库对象
"""
redis_store = StrictRedis(host=Config.REDIS_HOST, port=Config.REDIS_PORT, db=Config.REDIS_NUM)

"""
5：开启csrf后端保护机制
提取cookie中csrf_token和ajax请求头里面csrf_token进行验证操作
"""
csrf = CSRFProtect(app)

"""
6：创建session拓展类的对象
"""
Session(app)


@app.route('/')
def hello_world():
    """
    session调整存储方式
    没有调整之前，数据存在flask后端服务器，只是将session_id使用cookie的方式给了客户端
    :return:
    """
    session['name'] = "curry"

    return 'Hello World'


if __name__ == '__main__':
    app.run(debug=True)


