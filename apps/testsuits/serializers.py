#!/user/bin/even Python3
# -*- coding:utf-8 -*-
# serializers.py
# 测试套件序列化器
# author:zhaohexin
# time：2020/3/29 20:56


from rest_framework import serializers
from .models import Testsuits
from projects.models import Projects


class TestsuitesSerializer(serializers.ModelSerializer):
    """
    套件序列化器
    """
    # 转化中文
    project = serializers.StringRelatedField(label="所属项目", help_text="所属项目")
    project_id = serializers.PrimaryKeyRelatedField(queryset=Projects.objects.all(), label="项目id", help_text="项目id")

    class Meta:
        model = Testsuits
        # 指定所需字段
        fields = ("id", "name", "project", "project_id", "include", "create_time", "update_time")

        # 指定其他
        extra_kwargs = {
            "create_time": {
                "read_only": True
            },
            "update_time": {
                "read_only": True
            },
            "include": {
                "write_only": True
            }
        }

    def validate(self, attrs):
        """
        增加接口校验
        :param attrs:
        :return:
        """
        # 获取include并转换为list
        includes = eval(attrs.get("include"))
        # 转化成列表
        # TODO:变量列表ID进行接口表中是否需要校验
        if Projects.objects.filter(interfaces__id__in=includes):
            pass
        else:
            raise serializers.ValidationError("所选接口不存在！")
        return attrs

    def create(self, validated_data):
        validated_data["project_id"] = validated_data["project_id"].id
        testsuits_obj = super().create(validated_data)
        return testsuits_obj

    def update(self, instance, validated_data):
        if "project_id" in validated_data:
            validated_data["project_id"] = validated_data["project_id"].id
        testsuits_obj = super().update(instance, validated_data)
        return testsuits_obj
