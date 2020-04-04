# Create your views here.
import os
import time

from django.conf import settings
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from interfaces import models
from interfaces import serializers
from utils.tools import create_dir
from . import utils
from testcase.models import Testcases
from configures.models import Configures
from utils.execute_test_cases import create_testcase
from utils.execute_test_cases import run_testcase


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

    # 接口执行run方法
    @action(methods=["post"], detail=True)
    def run(self, request, *args, **kwargs):
        """
        接口执行run方法
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        # 获取模型类对象
        interface_obj = self.get_object()
        # 校验所传数据
        serializer = self.get_serializer(interface_obj, data=request.data)
        serializer.is_valid(raise_exception=True)
        # 获取env_id
        env_id = serializer.validated_data.get("env_id")
        # 生成主目录
        dir_time = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
        dir_path = os.path.join(settings.TESTCASE, dir_time)
        # 生成主目录、并进行相关校验
        if not create_dir(dir_path):
            return Response(data={"massages": f"生成 {dir_path} 目录失败，请重新尝试！！"}, status=status.HTTP_400_BAD_REQUEST)
        # 获取文件名 [当前执行用例名称]
        file_name = interface_obj.name + "测试"
        # 获取所有关联的用例列表对象
        testcase_obj_list = Testcases.objects.filter(interface_id=interface_obj.id)
        # 3、生产yml测试用例
        for testcase_obj in testcase_obj_list:
            create_testcases = create_testcase(testcase_obj, env_id, dir_path, file_name)
            if create_testcases.get("code") != 1:
                return Response(data={"massages": create_testcases.get("massages")}, status=status.HTTP_400_BAD_REQUEST)
        # 4、运行用例
        report_id = run_testcase(dir_path, file_name)
        return report_id

    # 从写serializer_class方法
    def get_serializer_class(self):
        """
        根据action方法返回不同的serializer方法
        :return:
        """
        if self.action == "run":
            return serializers.InterfaceRunSerializers
        else:
            return self.serializer_class
