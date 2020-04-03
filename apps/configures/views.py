from django.shortcuts import render
import json

from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from rest_framework.response import Response

from .models import Configures
from interfaces.models import Interfaces
from .serializers import ConfiguresSerializers
from utils import handle_datas


# Create your views here.

class ConfiguresViewSet(ModelViewSet):
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
    queryset = Configures.objects.all()
    serializer_class = ConfiguresSerializers
    # 权限
    permission_classes = [permissions.IsAuthenticated]
    # 筛选/排序
    filter_fields = ["id", "name"]
    ordering_fields = ["id", "name"]

    def retrieve(self, request, *args, **kwargs):
        # 获取配置信息
        configures_obj = self.get_object()

        # 获取配置请求信息
        configures_request = json.loads(configures_obj.request, encoding="utf-8")
        # 格式化 headers
        configures_headers = handle_datas.handle_data4(configures_request.get("config").get("request").get("headers"))
        # 格式化 globalVar
        configures_globa = handle_datas.handle_data2(configures_request.get("config").get("variables"))
        # 处理其他所需信息
        author = configures_obj.author
        configure_name = configures_obj.name
        selected_project_id = configures_obj.interface.project_id
        selected_interface_id = configures_obj.interface_id
        # 构造返回数据
        datas = {
            "author": author,
            "configure_name": configure_name,
            "selected_project_id": selected_project_id,
            "selected_interface_id": selected_interface_id,
            "header": configures_headers,
            "globalVar": configures_globa,

        }
        return Response(datas)
