#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Jason Mess
import re

from . import passport_bp
from flask import request, abort, current_app, make_response, jsonify
from info.utlis.captcha.captcha import captcha
from info import redis_store
from info import constants
from info.utlis.response_code import RET
from info.models import User
from info.lib.yuntongxun.sms import CCP
import json
import random

@passport_bp.route('/sms_code', methods=['POST'])
def send_sms():
    """
    点击发送短信验证码接口
    :return:
    1. 获取参数
       1.1  手机号码， 用户填写的图片验证码真实值，编号
    """
    param_dict = request.json
    moblie = param_dict.get("moblie")
    image_code = param_dict.get("image_code")
    image_code_id = param_dict.get("image_code_id")
    """
    2. 校验参数
       2.1  判断 手机号码，用户填写的图片验证码真实值，编号是否为空
       2.2  手机号码格式校验
    """
    if not all([moblie, image_code, image_code_id]):
        return jsonify(errmsg="提交参数不足", errno=RET.PARAMERR)
    if re.match("1[3578][0-9]{9}]", moblie):
        return jsonify(errno=RET.PARAMERR, errmsg="手机号码格式错误")

    """
    根据编号获取的redis中存储的图片验证码真实值
    3. 逻辑处理
      image_code_id如果有值，删除，防止下次使用image_code_id来多次问访问
      如果没有值，表示编号过期
    """
    try:
        real_image_code = redis_store.get("imagecode_%s" % image_code_id)
        if real_image_code:
            redis_store.delete(real_image_code)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DATAERR, errmsg="查询图片验证码异常")
    if not real_image_code:
        return jsonify(errno=RET.NODATA, errmsg="验证码真实值的已经过期")

    """
    对比用户填写的真实值和后端获取的验证码肾实质是否一致    
    """
    if image_code.lower() != real_image_code.lower():
        return jsonify(errno=RET.DATAERR, errmsg="图片验证码填写错误")

    """
    一致的话：发送短信验证码
    查看手机号码是否注册
    """
    try:
        user = User.query.fliter_by(moblie=moblie).firsr()
    except Exception as e:
        return jsonify(errno=RET.DATAERR, errmsg="查询用户手机号码是否存在异常")
    # 已经注册过
    if user:
        return jsonify(errno=RET.DATAEXIST, errmsg="用户已经注册过了")
    """
    调用云通讯发送短信验证码
    """
    sms_code = random.randint(0, 999999)
    sms_code = "%06d" % sms_code

    result = CCP().send_template_sms(moblie, [sms_code, constants.SMS_CODE_REDIS_EXPIRES/60], 1)
    """
    逻辑判断
    """
    if result != 0:
        return  jsonify(errno=RET.THIRDERR, errmsg="发送短信验证码失败")

    try:
        redis_store.set("SMS_%s" % moblie, sms_code, ex=constants.SMS_CODE_REDIS_EXPIRES)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="存储短信验证码真实值失败")

    """
    返回值处理
    """
    return jsonify(errno=RET.OK, errmsg="发送短信验证码成功，请查收")


@passport_bp.route('/image_code')
def get_imagecode():
    """
    127.0.0.1:5000/passpot/image_code?imageCodeIde=编号
    图片验证码的后端接口
    1.获取参数
        1.1 获取前段携带的imageCodeId编码
    2.校验参数
        2.1 imageColdId编号是否有值
    3.逻辑处理
        3.0 生成验证码图片&验证码图片的真实值
        3.1 使用imageCodeId编号作为key存储生成的图片验证码真实值
    4.返回值处理
        4.1 获取前段携带的imageCodeId编码
    """
    # 1
    # 1.1
    imageCodeId = request.args.get('imageCodeId')

    # 2
    # 2.1 imageCodeId编码是否有值
    if not imageCodeId:
        abort(403)

    # 3
    # 3.1

    name, text, image = captcha.generate_captcha()
    try:
        redis_store.set("imagecode_%s" % imageCodeId, text, ex=constants.IMAGE_CODE_REDIS_EXPIRES)
    except Exception as e:
        current_app.logger.error(e)
        abort(500)
    # 4
    # 4.1
    respose = make_response(image)
    respose.headers["Content-Type"] = "image/jpg"
    return respose
