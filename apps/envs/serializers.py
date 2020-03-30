#!/user/bin/even Python3
# -*- coding:utf-8 -*-
# serializers.py
# 序列化器定义
# author:zhaohexin
# time：2019/12/27 11:53 上午

from rest_framework import serializers
from . import models


class EnvsSerializers(serializers.ModelSerializer):
    """
    定义环境变量序列化器
    """

    class Meta:
        """
        设置元数据属性
        """
        # 设置自动生成模型
        model = models.EnvsModel
        # 排除更新时间校验
        fields = ("id", "name", "base_url", "create_time", "desc")
        extra_kwargs = {
            "create_time": {
                "read_only": True
            }
        }
