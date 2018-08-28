#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Jason Mess

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from redis import StrictRedis
from flask_wtf.csrf import CSRFProtect
from flask_session import Session
from config import config_dict
import logging
from logging.handlers import RotatingFileHandler
import pymysql
pymysql.install_as_MySQLdb()

"""
3：创建mysql数据库对象
并暴露给外界调用
当app没有值的时候，创建一个空的数据库对象
"""
db = SQLAlchemy()

"""
空数据库对象
type : 用来声明redis_store以后要保存
"""
redis_store = None  # type : StrictRedis


def create_log(config_name):
    """
    from logging.handlers import RotatingFileHandler
    记录日志的配置函数
    :return:
    设置日志的记录等级
    创建日志记录器，指明日志保存的路径、每个日志文件的最大大小、保存的日志文件个数上限
    创建日志记录的格式 日志等级 输入日志信息的文件名 行数 日志信息
    为刚创建的日志记录器设置日志记录格式
    为全局的日志工具对象（flask app使用的）添加日志记录器
    """
    logging.basicConfig(level=config_dict[config_name].LOG_LEVEL)  # 调试debug级

    file_log_handler = RotatingFileHandler("logs/log", maxBytes=100, backupCount=10)

    formatter = logging.Formatter('%(levelname)s %(filename)s:%(lineno)d %(message)s')

    file_log_handler.setFormatter(formatter)

    logging.getLogger().addHandler(file_log_handler)


"""
外界使用方式:create_app("development") --> 开发模式的app
          :create_app("production") --> 线上模式的app 
"""


def create_app(config_name):
    """
    记录日志
    """
    create_log(config_name)

    """
    生产app的工厂方法
    """
    app = Flask(__name__)

    """
    2：注册配置信息到app对象
    config_dict['development']----> 开发模式的配置
    config_dict['production']----> 生产模式的配置
    """
    configClass = config_dict[config_name]
    app.config.from_object(configClass)

    """
    3：创建mysql数据库对象
    """
    db.init_app(app)

    """
    4：创建redis数据库对象
    decode_responses=True 从redis获取的值是str类 
    """
    global redis_store
    redis_store = StrictRedis(host=configClass
                              .REDIS_HOST, port=configClass
                              .REDIS_PORT, db=configClass
                              .REDIS_NUM, decode_responses=True)

    """
    5：开启csrf后端保护机制
    提取cookie中csrf_token和ajax请求头里面csrf_token进行验证操作
    """
    csrf = CSRFProtect(app)

    """
    6：创建session拓展类的对象
    """
    Session(app)

    """
    导入蓝图（延迟导入：解决循环导入文件）
    注册蓝图
    """
    from info.modules.index import index_bp
    app.register_blueprint(index_bp)

    """
    登录注册模块
    """
    from info.modules.passport import passport_bp
    app.register_blueprint(passport_bp)


    return app
