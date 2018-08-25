#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Jason Mess
from redis import StrictRedis
import logging


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
    SQLALCHEMY_DATABASE_URI = "mysql://root:@127.0.0.1:3306/imformation16"
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
    SESSION_TYPE = "redis"
    """
    session需要数据加密
    设置不永久存储
    默认存储的有效时长
    """
    SESSION_USE_SIGNER = True
    SESSION_PERMANENT = False
    PERMANENT_SESSION_LIFETIME = 86400 * 2


class DevelopmentConfig(Config):
    """
    开发阶段的项目配置
    开启debug模式
    """
    DEBUG = True
    """
    设置日志级别
    """
    LOG_LEVEL = logging.debug("设置日志的级别")


class ProductionConfig(Config):
    """
    生产阶段的项目配置
    关闭debug模式
    """
    DEBUG = False

    """
    修改数据库的链接对象
    数据库链接配置
    SQLALCHEMY_DATABASE_URI = "mysql://root:cq@服务器ip地址:3306/information16"
    """


"""
使用方式：config_dict["development"]
公开一个接口给外界调用
"""
config_dict = {
    "development": DevelopmentConfig,
    "production": ProductionConfig
}

