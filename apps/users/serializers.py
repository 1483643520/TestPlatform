#!/user/bin/even Python3
# -*- coding:utf-8 -*-
# serializers.py
# 用户模型序序列化器校验
# author:zhaohexin
# time：2020/1/8 10:29 下午

import re
from rest_framework import serializers
from django.contrib.auth import models
from rest_framework.fields import CharField
from rest_framework.validators import UniqueValidator
from rest_framework_jwt.utils import api_settings


class UsersSerializers(serializers.ModelSerializer):
    password_confirm = CharField(label="确认密码", help_text="确认密码", max_length=128, write_only=True)
    token = CharField(label="token", help_text="token", max_length=128, read_only=True)

    class Meta:
        model = models.User
        fields = ("id", "username", "email", "password", "password_confirm", "token")
        write_only = ["email", "password"]
        extra_kwargs = {
            "username": {
                "label": "用户名",
                "help_text": "用户名",
                "min_length": 6,
                "max_length": 20,
                "error_messages": {
                    "min_length": "仅允许输入6-20个字符",
                    "max_length": "仅允许输入6-20个字符",
                }

            },
            "email": {
                "label": "邮箱",
                "help_text": "邮箱",
                "write_only": True,
                "required": True,
                "validators": [UniqueValidator(queryset=models.User.objects.all(), message="此邮箱已被注册")]
            },
            "password": {
                "label": "密码",
                "help_text": "密码",
                "min_length": 6,
                "max_length": 20,
                "write_only": True,
                "error_messages": {
                    "min_length": "仅允许输入6-20个字符",
                    "max_length": "仅允许输入6-20个字符",
                }
            },
        }

    def validate(self, attrs):
        password_ = attrs["password_confirm"]
        if attrs["password"] != password_:
            raise serializers.ValidationError("密码与确认密码必须一致")
        del attrs["password_confirm"]
        return attrs

    def create(self, validated_data):
        # 重置加密密码
        # create_user会对密码进行加密
        user = models.User.objects.create_user(**validated_data)
        # 生成token
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        user.token = token
        return user
