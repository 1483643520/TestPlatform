#!/user/bin/even Python3
# -*- coding:utf-8 -*-
# serializers.py
# 配置模块序列化器
# author:zhaohexin
# time：2020/3/30 18:53


from rest_framework import serializers
from .models import Configures
from interfaces.models import Interfaces
from projects.models import Projects


class InterfaceOtherSerializers(serializers.ModelSerializer):
    """
    需要关联的项目信息
    """
    # 确定project名称及ID
    project = serializers.StringRelatedField(label="所属项目名称", help_text="所属项目名称")
    project_id = serializers.PrimaryKeyRelatedField(queryset=Projects.objects.all(), write_only=True,
                                                    help_text="所属项目ID", label="所属项目ID")
    # 从新定义interface ID，避免和用例ID重复
    interface_id = serializers.PrimaryKeyRelatedField(queryset=Interfaces.objects.all(), write_only=True,
                                                      help_text="所属接口ID", label="所属接口ID")

    class Meta:
        model = Interfaces
        # 确定需要字段
        fields = ("name", "project", "project_id", "interface_id")

        extra_kwargs = {
            "name": {
                "read_only": True
            },

        }

    # TODO:校验所传project_id，interface_id是否存在且相互匹配
    # def validate(self, attrs):
    #     return attrs
    #     pass


class ConfiguresSerializers(serializers.ModelSerializer):
    """
    配置模块序列化器
    """
    # 导入所需信息
    interface = InterfaceOtherSerializers(label="所属项目和接口信息", help_text="所属项目接口信息")

    class Meta:
        model = Configures
        # 指定需要字段
        fields = ("id", "name", "author", "request", "interface")
        # 指定特殊规则
        extra_kwargs = {
            "request": {
                "write_only": True
            },
        }

    # 从写create/update方法
    def create(self, validated_data):
        if "interface" in validated_data:
            interfaces = validated_data.pop("interface")
            validated_data["interface_id"] = interfaces["interface_id"].id
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if "interface" in validated_data:
            interfaces = validated_data.pop("interface")
            validated_data["interface_id"] = interfaces["interface_id"].id
        return super().update(instance, validated_data)
