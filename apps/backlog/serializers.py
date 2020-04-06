#!/user/bin/even Python3
# -*- coding:utf-8 -*-
# serializers.py
# 配置模块序列化器
# author:zhaohexin
# time：2020/3/30 18:53


from rest_framework import serializers
from .models import BacklogModel


class BacklogSerializers(serializers.ModelSerializer):
    """
    配置模块序列化器
    """

    class Meta:
        model = BacklogModel
        # 指定需要字段
        fields = ("id", "text", "status", "user", "update_time")
        # 指定特殊规则
        extra_kwargs = {
        }

