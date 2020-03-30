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


def format_time_by_testsuits(datas):
    """
    1、对时间进行格式化
    :param datas:
    :return:
    """
    datas_list = []
    for item in datas:
        create_time = item["create_time"]
        item["create_time"] = create_time.split("T")[0] + " " + create_time.split("T")[1].split(".")[0]
        update_time = item["update_time"]
        item["update_time"] = update_time.split("T")[0] + " " + update_time.split("T")[1].split(".")[0]

        datas_list.append(item)

    return datas_list
