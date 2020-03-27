from django.shortcuts import render

# Create your views here.
# Create your views here.
from rest_framework import viewsets, permissions
from rest_framework import generics

from django.contrib.auth import models
from rest_framework.decorators import action
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from users import serializers


class UsersViewSet(viewsets.ModelViewSet):
    """
    create:
    创建项目

    list:
    获取结果集

    retrieve:
    获取具体一条接口信息

    update:
    全字段更新

    partial_update:
    个别字段更新

    destroy：
    删除接口

    """
    
    # 定义 queryset 查询集
    queryset = models.User.objects.all()
    # 定义 serializer_class 序列化器类
    serializer_class = serializers.UsersSerializers
    """
    # 定义过滤引擎，排序引擎，分页引擎,也可以在setting中设置默认项,此项目在setting中配置，一下为类中配置
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    pagination_class = [PageNumberPagination]
    """
    # 定义筛选字段
    filterset_fields = ["id", "username", "email"]
    # 定义排序字段
    ordering_fields = ["id"]
    # 定义授权类
    permission_classes = [permissions.IsAuthenticated]


class Check(GenericAPIView):
    
    def get(self, request, pk):
        """
        校验用户名及邮箱是否重复s
        :param request:
        :param pk:
        :return:
        """
        if "@" in pk:
            print(pk)
            emails = models.User.objects.all().filter(email = pk)
            result = {
                "count": len(emails)
            }
            return Response(data = result)
        else:
            emails = models.User.objects.all().filter(username = pk)
            result = {
                "count": len(emails)
            }
            return Response(data = result)
