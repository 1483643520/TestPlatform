# Create your views here.
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from . import models
from . import serializers


class DebugtalksViewSet(viewsets.ModelViewSet):
    """

    list:
    获取结果集

    update:
    全字段更新

    """

    # 定义 queryset 查询集
    queryset = models.DebugTalksModel.objects.all()
    # 定义 serializer_class 序列化器类
    serializer_class = serializers.DebugtalksSerializers
    """
    # 定义过滤引擎，排序引擎，分页引擎,也可以在setting中设置默认项,此项目在setting中配置，一下为类中配置
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    pagination_class = [PageNumberPagination]
    """
    # 定义筛选字段
    filterset_fields = ["id", "name", "project_id", "create_time"]
    # 定义排序字段
    ordering_fields = ["id", "name", "project_id"]
    # 登录才能操作
    permission_classes = [permissions.IsAuthenticated]
