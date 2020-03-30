#!/user/bin/even Python3
# -*- coding:utf-8 -*-
# serializers.py
# 报告序列化器
# author:zhaohexin
# time：2020/3/29 20:56


from rest_framework import serializers
from .models import ReportsModel


class ReportsSerializer(serializers.ModelSerializer):
    """
    报告序列化器
    """

    class Meta:
        model = ReportsModel
        # 排除不需字段
        exclude = ("update_time",)

        # 指定其他
        extra_kwargs = {
            "create_time": {
                "read_only": True
            },
        }
