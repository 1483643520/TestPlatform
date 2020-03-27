#!/user/bin/even Python3
# -*- coding:utf-8 -*-
# jwt_handler.py
# 登录验证返回值修改
# author:zhaohexin
# time：2020/1/12 3:24 下午

def jwt_response_payload_handler(token, user = None, request = None):
    return {
        "token": token,
        "user_id": user.id,
        "username": user.username
    }
