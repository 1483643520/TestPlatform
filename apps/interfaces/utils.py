#!/user/bin/even Python3
# -*- coding:utf-8 -*-
# utils.py
# 工具类
# author:zhaohexin
# time：2020/2/19 3:11 下午
import datetime
from django.db.models import Count
from testcase.models import Testcases
from configures.models import Configures


def get_count_by_project(datas):
    """
    1、计算当前接口所关联的配置数及用例数
    2、对时间进行格式化
    :param datas:
    :return:
    """
    datas_list = []
    for item in datas:
        create_time = item["create_time"]
        item["create_time"] = create_time.split("T")[0] + " " + create_time.split("T")[1].split(".")[0]

        # 获取用例数量
        interface_id = item["id"]
        testcase_count = Testcases.objects.filter(interface_id=interface_id).count()
        # 获取配置数量
        configures_count = Configures.objects.filter(interface_id=interface_id).count()

        item["testcases"] = testcase_count
        item["configures"] = configures_count

        datas_list.append(item)

    return datas_list
