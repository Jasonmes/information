#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Jason Mess

from flask import Flask, session, current_app
from flask_script import Manager
from info import create_app, db
from flask_migrate import Migrate, MigrateCommand
import logging

"""
单一职责的原则：manage.py 仅仅作为项目启动文件
整体业务逻辑都在info那里
"""

"""
7: 创建manager管理类
"""
app = create_app("development")
manager = Manager(app)

"""
初始化迁移对象
将迁移命令添加到管理对象中
"""
Migrate(app, db)
manager.add_command("db", MigrateCommand)


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
    """
    python manage.py runserver -h -p -d
    """
    logging.debug("debug的信息")
    logging.info("info的信息")
    logging.warning("debug的信息")
    logging.error("errord的日志信息")
    logging.critical("erro的日志信息")

    # current_app.logger.info('使用current_app封装好的info的信息')

    manager.run()
