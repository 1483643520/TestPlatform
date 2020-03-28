#!/user/bin/even Python3
# -*- coding:utf-8 -*-
# utils.py
# 工具类
# author:zhaohexin
# time：2020/2/19 3:11 下午
import datetime
from django.db.models import Count
from interfaces.models import Interfaces
from testcase.models import Testcases
from testsuits.models import Testsuits
from configures.models import Configures


def get_count_by_project(datas):
    """
    1、通过项目中的接口、用例、配置、套件的数量
    2、对时间进行格式化
    :param datas:
    :return:
    """
    datas_list = []
    for item in datas:
        create_time = item["create_time"]
        item["create_time"] = create_time.split("T")[0] + " " + create_time.split("T")[1].split(".")[0]

        # 获取接口数量
        # 分组关联计数
        project_id = item["id"]
        interface_testcases_objs = Interfaces.objects.values("id").annotate(testcases=Count("testcases")).filter(
            project_id=project_id)
        # 获取接口数量
        interfaces_count = interface_testcases_objs.count()
        # 获取用例总数
        testcases_count = 0
        for i in interface_testcases_objs:
            testcases_count += i["testcases"]
        # 获取配置数量
        interface_configures_objs = Interfaces.objects.values("id").annotate(configures=Count("configures")).filter(
            project_id=project_id)
        configures_count = 0
        for i in interface_configures_objs:
            configures_count += i["configures"]
        # 获取套件总数
        testsuits_count = Testsuits.objects.filter(project_id=project_id).count()

        item["interfaces"] = interfaces_count
        item["testsuits"] = testsuits_count
        item["testcases"] = testcases_count
        item["configures"] = configures_count

        datas_list.append(item)

    return datas_list
