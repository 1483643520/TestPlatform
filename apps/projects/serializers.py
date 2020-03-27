#!/user/bin/even Python3
# -*- coding:utf-8 -*-
# serializers.py
# 序列化器定义
# author:zhaohexin
# time：2019/12/27 11:53 上午

from rest_framework import serializers

from debugtalks.models import DebugTalks
from . import models


class ProjectsModelSerializers(serializers.ModelSerializer):
    """
    定义项目序列化器
    """
    
    class Meta:
        """
        设置元数据属性
        """
        # 设置自动生成模型
        model = models.Projects
        # 排除更新时间校验
        exclude = ("update_time",)
        extra_kwargs = {
            "create_time": {
                "read_only": True
            }
        }
    
    def create(self, validate_data):
        project_obj = super().create(validate_data)
        DebugTalks.objects.create(project = project_obj)
        return project_obj
