#!/user/bin/even Python3
# -*- coding:utf-8 -*-
# serializers.py
# 序列化器定义
# author:zhaohexin
# time：2019/12/27 11:53 上午

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from projects.models import Projects
from interfaces.models import Interfaces
from . import models


# 自定义接口校验
def name_check(value):
    """
    自定义名称校验
    @param value: name值
    @return: raise 报错信息
    """
    if not value.endswith("接口"):
        raise serializers.ValidationError("接口名称必须以 '接口'为结尾")


class ProjectsModelSerializers(serializers.ModelSerializer):
    """
    定义父表序列化器
    """
    
    class Meta:
        model = Projects
        fields = "__all__"


class InterfacesModelSerializers(serializers.ModelSerializer):
    """
    定义接口模型序列化器
    """
    # 获取父表信息
    # project = ProjectsModelSerializers(label = "父项目信息", read_only = True)
    
    class Meta:
        """
        设置元数据属性
        """
        # 设置自动生成模型
        model = models.Interfaces
        # 排除更新时间校验
        exclude = ("create_time", "update_time")
        # 重置说明
        extra_kwargs = {
            "project": {
                "write_only": True
            },
            "name": {"validators": [UniqueValidator(queryset = models.Interfaces.objects.all()), name_check]},
        }
    
    def validate_name(self, value):
        if '校验' not in value:
            raise serializers.ValidationError("接口名称必须包含 '校验' ")
        return value
    
    def validate(self, attrs):
        if '测试' not in attrs["name"] and "测试" not in attrs["tester"]:
            raise serializers.ValidationError("接口名称或负责人必须包含 '测试' ")
        return attrs
    
    # def create(self, validated_data):
    #     """
    #     从新定义新增对象
    #     @param validated_data: 需要新增的数据
    #     @return:返回新增后的数据
    #     """
    #     # 判断外键是否在主表中存在
    #     # 获取主表所有id
    #     print(validated_data)
    #     project_value = Projects.objects.get(id = validated_data["project"])
    #     if project_value:
    #         # 将project变成project对象
    #         validated_data["project"] = Projects(validated_data["project"])
    #         Interfaces.objects.create(**validated_data)
    #         validated_data["project"] = project_value
    #         return validated_data
