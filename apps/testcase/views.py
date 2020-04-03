import json
import time
import os

from django.conf import settings
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions, status
from rest_framework.response import Response

from .models import Testcases
from interfaces.models import Interfaces
from .serializers import TestcasesSerializers
from utils import handle_datas
from .serializers import TestcaseRunSerializers
from utils.tools import create_dir
from utils.execute_test_cases import create_testcase
from utils.execute_test_cases import run_testcase
from reports.models import ReportsModel


class TestcasesViewSet(ModelViewSet):
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
    queryset = Testcases.objects.all()
    serializer_class = TestcasesSerializers
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ["id", "name"]
    ordering_fields = ('id', 'name')

    def retrieve(self, request, *args, **kwargs):
        """获取用例详情信息"""
        testcase_obj = self.get_object()

        # 用例前置信息
        testcase_include = json.loads(testcase_obj.include, encoding='utf-8')

        # 用例请求信息
        testcase_request = json.loads(testcase_obj.request, encoding='utf-8')
        testcase_request_datas = testcase_request.get('test').get('request')

        # 处理用例的validate列表
        # 将[{'check': 'status_code', 'expected':200, 'comparator': 'equals'}]
        # 转化为[{key: 'status_code', value: 200, comparator: 'equals', param_type: 'string'}]
        testcase_validate = testcase_request.get('test').get('validate')
        testcase_validate_list = handle_datas.handle_data1(testcase_validate)

        # 处理用例的param数据
        testcase_params = testcase_request_datas.get('params')
        testcase_params_list = handle_datas.handle_data4(testcase_params)

        # 处理用例的header列表
        testcase_headers = testcase_request_datas.get('headers')
        testcase_headers_list = handle_datas.handle_data4(testcase_headers)

        # 处理用例variables变量列表
        testcase_variables = testcase_request.get('test').get('variables')
        testcase_variables_list = handle_datas.handle_data2(testcase_variables)

        # 处理form表单数据
        testcase_form_datas = testcase_request_datas.get('data')
        testcase_form_datas_list = handle_datas.handle_data6(testcase_form_datas)

        # 处理json数据
        # testcase_json_datas = str(testcase_request_datas.get('json'))
        testcase_json_datas = json.dumps(testcase_request_datas.get('json'), ensure_ascii=False)

        # 处理extract数据
        testcase_extract_datas = testcase_request.get('test').get('extract')
        testcase_extract_datas_list = handle_datas.handle_data3(testcase_extract_datas)

        # 处理parameters数据
        testcase_parameters_datas = testcase_request.get('test').get('parameters')
        testcase_parameters_datas_list = handle_datas.handle_data3(testcase_parameters_datas)

        # 处理setupHooks数据
        testcase_setup_hooks_datas = testcase_request.get('test').get('setup_hooks')
        testcase_setup_hooks_datas_list = handle_datas.handle_data5(testcase_setup_hooks_datas)

        # 处理teardownHooks数据
        testcase_teardown_hooks_datas = testcase_request.get('test').get('teardown_hooks')
        testcase_teardown_hooks_datas_list = handle_datas.handle_data5(testcase_teardown_hooks_datas)

        selected_configure_id = testcase_include.get('config')
        selected_interface_id = testcase_obj.interface_id
        selected_project_id = Interfaces.objects.get(id=selected_interface_id).project_id
        selected_testcase_id = testcase_include.get('testcases')

        datas = {
            "author": testcase_obj.author,
            "testcase_name": testcase_obj.name,
            "selected_configure_id": selected_configure_id,
            "selected_interface_id": selected_interface_id,
            "selected_project_id": selected_project_id,
            "selected_testcase_id": selected_testcase_id,

            "method": testcase_request_datas.get('method'),
            "url": testcase_request_datas.get('url'),
            "param": testcase_params_list,
            "header": testcase_headers_list,
            "variable": testcase_form_datas_list,  # form表单请求数据
            "jsonVariable": testcase_json_datas,

            "extract": testcase_extract_datas_list,
            "validate": testcase_validate_list,
            "globalVar": testcase_variables_list,  # 变量
            "parameterized": testcase_parameters_datas_list,
            "setupHooks": testcase_setup_hooks_datas_list,
            "teardownHooks": testcase_teardown_hooks_datas_list,
        }
        return Response(datas)

    # TODO:需要run方法执行用例
    @action(methods=["POST"], detail=True)
    def run(self, request, *args, **kwargs):
        # 1、获取模型类对象
        testcase_obj = self.get_object()
        # 2、校验
        serializer = self.get_serializer(testcase_obj, data=request.data)
        serializer.is_valid(raise_exception=True)
        # 获取env_id
        env_id = serializer.validated_data.get("env_id")
        # 生成主目录
        # 获取时间戳
        dir_time = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
        dir_path = os.path.join(settings.TESTCASE, dir_time)
        # 生成主目录、并进行相关校验
        if not create_dir(dir_path):
            return Response(data={"massages": f"生成 {dir_path} 目录失败，请重新尝试！！"}, status=status.HTTP_400_BAD_REQUEST)
        # 获取文件名 [当前执行用例名称]
        file_name = testcase_obj.name + "测试"
        # 3、生产yml测试用例
        create_testcases = create_testcase(testcase_obj, env_id, dir_path, file_name)
        if create_testcases.get("code") != 1:
            return Response(data={"massages": create_testcases.get("massages")}, status=status.HTTP_400_BAD_REQUEST)

        # 4、运行用例
        report_id = run_testcase(dir_path, file_name)
        return report_id

    def get_serializer_class(self):
        """
        根据action方法返回不同的serializer方法
        :return:
        """
        if self.action == "run":
            return TestcaseRunSerializers
        else:
            return self.serializer_class
