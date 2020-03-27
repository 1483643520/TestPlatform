# Create your views here.
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from projects import models
from projects import serializers
from .utils import get_count_by_project

class ProjectsViewSet(viewsets.ModelViewSet):
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
    queryset = models.Projects.objects.all()
    # 定义 serializer_class 序列化器类
    serializer_class = serializers.ProjectsModelSerializers
    """
    # 定义过滤引擎，排序引擎，分页引擎,也可以在setting中设置默认项,此项目在setting中配置，一下为类中配置
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    pagination_class = [PageNumberPagination]
    """
    # 定义筛选字段
    filterset_fields = ["id", "name"]
    # 定义排序字段
    ordering_fields = ["id", "name"]
    permission_classes = [permissions.IsAuthenticated]
    
    # 重写list方法
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many = True)
            # 对结果进行格式化
            datas = get_count_by_project(serializer.data)
            return self.get_paginated_response(datas)
        serializer = self.get_serializer(queryset, many = True)
        return Response(serializer.data)
    
    # 获取项目所有名称
    @action(methods = ["get"], detail = False)
    def name(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(instance = queryset, many = True)
        return Response(serializer.data)
    
    # 获取项目接口信息
    @action(detail = True)
    def interfaces(self, request, *args, **kwargs):
        instance = self.get_queryset()
        serializer = self.get_serializer(instance = instance, many = True)
        return Response(serializer.data)
    
    # 从写 get_serializer_class 方法
    def get_serializer_class(self):
        return serializers.ProjectsInterfacesModelSerializers if self.action == "interfaces" \
            else self.serializer_class
