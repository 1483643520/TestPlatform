# Create your views here.
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from interfaces import models
from interfaces import serializers
from . import utils
from testcase.models import Testcases
from configures.models import Configures


class InterfacesViewSet(viewsets.ModelViewSet):
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
    queryset = models.Interfaces.objects.all()
    # 定义 serializer_class 序列化器类
    serializer_class = serializers.InterfacesSerializers
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

    # 重写list方法，实现查找用例数，配置数及时间格式化
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        response.data["results"] = utils.get_count_by_project(response.data["results"])
        return response

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    # 获取接口所属用例信息
    @action(methods=["get"], detail=True)
    def testcases(self, request, pk=None):
        # 根据传入ID值进行搜索
        testcases_obj = Testcases.objects.filter(interface_id=pk)
        # 进行迭代取出id和name
        testcases_list = []
        for obj in testcases_obj:
            testcases_list.append({"id": obj.id, "name": obj.name})

        return Response(data=testcases_list)

    # 获取接口对应配置信息
    @action(methods=["get"], detail=True)
    def configs(self, request, pk=None):
        # 根据传入ID值进行搜索
        configs_obj = Configures.objects.filter(interface_id=pk)
        # 进行迭代取出id和name
        configs_list = []
        for obj in configs_obj:
            configs_list.append({"id": obj.id, "name": obj.name})

        return Response(data=configs_list)
