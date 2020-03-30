from django.shortcuts import render

# Create your views here.

from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from . import models
from . import serializers
from . import utils


class EnvsViewSet(viewsets.ModelViewSet):
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
    queryset = models.EnvsModel.objects.all()
    # 定义 serializer_class 序列化器类
    serializer_class = serializers.EnvsSerializers
    """
    # 定义过滤引擎，排序引擎，分页引擎,也可以在setting中设置默认项,此项目在setting中配置，一下为类中配置
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    pagination_class = [PageNumberPagination]
    """
    # 定义筛选字段
    filterset_fields = ["id", "name", "base_url", "create_time", "desc"]
    # 定义排序字段
    ordering_fields = ["id", "name", "base_url", "create_time", "desc"]
    # 登录才能操作
    permission_classes = [permissions.IsAuthenticated]

    # 从新定义list查询
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        response.data["results"] = utils.format_time_by_envs(response.data["results"])
        return response

    # 获取环境名称
    @action(methods=["get"], detail=False)
    def names(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(instance=queryset, many=True)
        return Response(serializer.data)
