import json

from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from rest_framework.response import Response

from . import utils
from .models import BacklogModel
from .serializers import BacklogSerializers

# Create your views here.
from .utils import format_time_by_backlog


class BacklogViewSet(ModelViewSet):
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
    queryset = BacklogModel.objects.all()
    serializer_class = BacklogSerializers
    # 权限
    permission_classes = [permissions.IsAuthenticated]
    # 筛选/排序
    filter_fields = ["id", "update_time", "user_id"]
    ordering_fields = ["update_time"]

    # 重写list方法，将时间进行转换
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset().order_by("status")).order_by("create_time")
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        datas = self.get_paginated_response(serializer.data)
        datas.data["results"] = format_time_by_backlog(datas.data["results"])
        return datas

    def create(self, request, *args, **kwargs):
        obj = super().create(request, *args, **kwargs)
        pass
        return obj
