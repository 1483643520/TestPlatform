# Create your views here.
import os
import time

from django.conf import settings
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from testcase.models import Testcases
from utils.execute_test_cases import create_testcase, run_testcase
from utils.tools import create_dir
from . import models
from . import serializers
from .utils import get_count_by_project
from interfaces.models import Interfaces


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
    filterset_fields = ["id", "name", "leader", "tester"]
    # 定义排序字段
    ordering_fields = ['id', 'name', 'leader']
    permission_classes = [permissions.IsAuthenticated]

    # 重写list方法
    def list(self, request, *args, **kwargs):
        # queryset = self.filter_queryset(self.get_queryset())
        #
        # page = self.paginate_queryset(queryset)
        # if page is not None:
        #     serializer = self.get_serializer(page, many=True)
        #     # 对结果进行格式化
        #     datas = get_count_by_project(serializer.data)
        #     return self.get_paginated_response(datas)
        # serializer = self.get_serializer(queryset, many=True)
        # return Response(serializer.data)
        # 调用父类方法
        response = super().list(request, *args, **kwargs)
        # 覆盖原有数据进行新数据组装
        response.data["results"] = get_count_by_project(response.data["results"])
        return response

    # 获取项目所有名称
    @action(methods=["get"], detail=False)
    def names(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(instance=queryset, many=True)
        return Response(serializer.data)

    # 获取项目接口信息
    @action(detail=True)
    # 使用序列化器方法
    # def interfaces(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     # 使用序列化器方法
    #     # serializer = self.get_serializer(instance=instance)
    #     # 更加定制化方法
    #     Interface
    #     return Response(serializer.data)

    # 使用定制化方法
    def interfaces(self, request, pk=None):
        # 根据传入ID值进行搜索
        interface_obj = Interfaces.objects.filter(project_id=pk)
        # 进行迭代取出id和name
        interface_list = []
        for obj in interface_obj:
            interface_list.append({"id": obj.id, "name": obj.name})

        return Response(data=interface_list)

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
        project_obj = self.get_object()
        # 校验所传数据
        serializer = self.get_serializer(project_obj, data=request.data)
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
        file_name = project_obj.name + "测试"
        # 获取所有关联的用例列表对象
        for interfaces in Interfaces.objects.filter(project_id=project_obj.id):
            testcase_obj_list = Testcases.objects.filter(interface_id=interfaces.id)
            # 3、生产yml测试用例
            for testcase_obj in testcase_obj_list:
                create_testcases = create_testcase(testcase_obj, env_id, dir_path, file_name)
                if create_testcases.get("code") != 1:
                    return Response(data={"massages": create_testcases.get("massages")},
                                    status=status.HTTP_400_BAD_REQUEST)
        # 4、运行用例
        report_id = run_testcase(dir_path, file_name)
        return report_id

    # 从写 get_serializer_class 方法
    def get_serializer_class(self):
        # 根据不同接口调用返回不同的数据
        if self.action == "names":
            return serializers.ProjectsNameSerializer
        elif self.action == "interfaces":
            return serializers.InterfacesByProjectIdSerializer
        elif self.action == "run":
            return serializers.ProjectRunSerializers
        else:
            return self.serializer_class
