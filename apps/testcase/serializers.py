#!/user/bin/even Python3
# -*- coding:utf-8 -*-
# serializers.py
# 用例模块序列化器
# author:zhaohexin
# time：2020/3/30 18:53


from rest_framework import serializers
from .models import Testcases
from interfaces.models import Interfaces
from projects.models import Projects
from envs.models import EnvsModel


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
        fields = ("id", "name", "project", "project_id", "interface_id")

        extra_kwargs = {
            "name": {
                "read_only": True
            },

        }

    # TODO:校验所传project_id，interface_id是否存在且相互匹配
    # def validate(self, attrs):
    #     return attrs
    #     pass


class TestcasesSerializers(serializers.ModelSerializer):
    """
    用例模块序列化器
    """
    # 导入所需信息
    interface = InterfaceOtherSerializers(label="所属项目和接口信息", help_text="所属项目接口信息")

    class Meta:
        model = Testcases
        # 指定需要字段
        fields = ("id", "name", "include", "author", "request", "interface")
        # 指定特殊规则
        extra_kwargs = {
            "include": {
                "write_only": True
            },
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


# 定义全局环境变量序列化校验器
class TestcaseRunSerializers(serializers.ModelSerializer):
    """
    定义全局环境变量序列化校验器
    """
    env_id = serializers.IntegerField(write_only=True, label="全局变量ID", help_text="全局变量ID")

    class Meta:
        model = Testcases
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
            raise serializers.ValidationError("所选环境不存在！")
