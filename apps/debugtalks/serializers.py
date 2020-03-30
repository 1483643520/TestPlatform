#!/user/bin/even Python3
# -*- coding:utf-8 -*-
# serializers.py
# 序列化器定义
# author:zhaohexin
# time：2019/12/27 11:53 上午

from rest_framework import serializers

from projects.models import Projects
from . import models


class DebugtalksSerializers(serializers.ModelSerializer):
    """
    定义配置函数序列化器
    """
    # 获取父表项目名称，默认read_only=true
    project = serializers.StringRelatedField(label="所属项目名称", help_text="所属项目名称")
    # 从新指认项目ID
    project_id = serializers.PrimaryKeyRelatedField(queryset=Projects.objects.all(), label="项目ID", help_text="项目ID",
                                                    write_only=True)

    class Meta:
        """
        设置元数据属性
        """
        # 设置自动生成模型
        model = models.DebugTalksModel
        # 排除更新时间校验
        fields = ("id", "name", "debugtalk", "create_time", "project_id", "project")
        extra_kwargs = {
            "create_time": {
                "read_only": True
            }
        }

    def update(self, instance, validated_data):
        response = super().update(instance, validated_data)
        return response
