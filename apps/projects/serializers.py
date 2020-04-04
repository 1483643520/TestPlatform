#!/user/bin/even Python3
# -*- coding:utf-8 -*-
# serializers.py
# 序列化器定义
# author:zhaohexin
# time：2019/12/27 11:53 上午

from rest_framework import serializers

from debugtalks.models import DebugTalksModel
from envs.models import EnvsModel
from . import models
from interfaces.models import Interfaces


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
        # 对应创建debugTalks数据
        DebugTalksModel.objects.create(project=project_obj)
        return project_obj


class ProjectsNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Projects
        fields = ("id", "name")


class InterfaceNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interfaces
        fields = ("id", "name")


class InterfacesByProjectIdSerializer(serializers.ModelSerializer):
    interfaces = InterfaceNameSerializer(read_only=True, many=True)

    class Meta:
        model = models.Projects
        fields = ("id", "interfaces")


# 定义全局环境变量序列化校验器
class ProjectRunSerializers(serializers.ModelSerializer):
    """
    定义全局环境变量序列化校验器
    """
    env_id = serializers.IntegerField(write_only=True, label="全局变量ID", help_text="全局变量ID")

    class Meta:
        model = models.Projects
        fields = ("id", "env_id")

    def validate(self, attrs):
        """
        校验 env_id是否存在
        :param attrs: 传入参数attrs
        :return:传出参数attrs
        """
        # 判断env_id是否存在
        if EnvsModel.objects.filter(id=attrs.get("env_id")).exists():
            return attrs
        else:
            raise serializers.ValidationError("所选接口不存在！")

