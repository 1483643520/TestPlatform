# !/user/bin/even Python3
# -*- coding:utf-8 -*-
# execute_test_cases.py
# 创建并执行ymal用例，生成测试报告并存储数据库
# author:zhaohexin
# time：2020/4/1 11:34
import logging
import os
import json
from datetime import datetime

import yaml
from httprunner.api import HttpRunner
from httprunner import report
from httprunner.exceptions import ParamsError
from rest_framework import status
from rest_framework.response import Response

from utils.tools import create_dir
from configures.models import Configures
from envs.models import EnvsModel
from testcase.models import Testcases
from debugtalks.models import DebugTalksModel
from reports.models import ReportsModel

logger = logging.getLogger('test')


def create_testcase(obj, env_id, dir_path, file_name):
    """
    创建单条用例（包括前置用例）yml文件
    :param obj: 用例 模型类对象
    :param env_id: 所选全局变量id
    :param dir_path: 存放主目录
    :param file_name: 全局变量/yml 名称
    :return:
    """
    # 生成文件目录
    # 1.获取项目名称
    project_name = obj.interface.project.name
    interface_name = obj.interface.name
    # 2.生成文件目录
    file_dir = os.path.join(dir_path, project_name, interface_name)
    # 创建debugtalk文件
    if not os.path.exists(file_dir):
        create_dir(file_dir)
        debugtalk_obj = DebugTalksModel.objects.filter(project__name=project_name).first()
        if debugtalk_obj:
            debugtalk = debugtalk_obj.debugtalk
        else:
            debugtalk = ""

        # 创建debugtalk.py文件
        with open(os.path.join(os.path.join(dir_path, project_name), 'debugtalk.py'),
                  mode='w',
                  encoding='utf-8') as one_file:
            one_file.write(debugtalk)
    # 组装文件目录
    file_path = os.path.join(file_dir, file_name + ".yml")
    # 定义外层列表数据结构
    yml = {"config": None, "teststeps": None}
    # 拼接 config 模块
    config = generate_config(json.loads(obj.include).get("config"), env_id, file_name)
    # 拼接 teststeps 模块
    teststeps = generate_teststeps(obj)
    # 组装最后文件内容
    yml["config"] = config
    yml["teststeps"] = teststeps
    # 写入yml文件
    with open(file_path,
              mode="w", encoding="utf-8") as one_file:
        yaml.dump(yml, one_file, allow_unicode=True, default_flow_style=False)

    return {"code": 1, "messages": f"生成yml文件成功 {file_path}"}


def generate_config(config_id, env_id, file_name):
    """
    拼接 yml 文件config 全局变量模块
    :param file_name: 全局变量名称
    :param config_id: 用例所关联的config_id
    :param env_id: 用户所选择好的全局环境变量id
    :return: 返回组装好的config模块，字典形式
    """
    config = {"config": {"request": {}}}
    # 获取 config 信息
    if config_id is not None:
        config = json.loads(Configures.objects.get(id=config_id).request)
        # 获取 base_url
    base_url = EnvsModel.objects.get(id=env_id).base_url
    # 组装 config 信息
    config["config"]["base_url"] = base_url
    config["config"]["name"] = file_name
    return config["config"]


def generate_teststeps(obj):
    """
    组装 teststeps 模块
    :param pre_list:
    :param obj: testcase 模型类对象
    :return: 返回组装好的 testcase
    """
    # 创建前置列表
    pre_list = []
    # 获取需要执行当前用例的所有用例ID
    pre_list = generate_pre(obj, pre_list)
    # 创建 teststeps 列表
    teststeps = []
    # 批量循环并组装 teststeps
    for pre_id in pre_list:
        testcase = generate_testcase(pre_id)
        teststeps.append(testcase)
    return teststeps


def generate_pre(obj, pre_list):
    """
    每次循环的前置用例列表集合
    :param obj: 需要获取前置列表的 testcase 模型类对象
    :param pre_list:前置用例列表
    :return:返回前置用例列表
    """
    if json.loads(obj.include).get("testcases"):
        for pre_id in json.loads(obj.include).get("testcases"):
            # 判断当前 pre_id 是否还有前置用例
            if json.loads(Testcases.objects.get(id=pre_id).include).get("testcases"):
                generate_pre(Testcases.objects.get(id=pre_id), pre_list)
            else:
                pre_list.append(pre_id)
            # 判断当前循环是否为当前前置列表最后一个，若是，加上当前用例ID
            if pre_id == json.loads(obj.include).get("testcases")[-1]:
                pre_list.append(obj.id)
    else:
        pre_list.append(obj.id)
    return pre_list


def generate_testcase(pr_id):
    """
    单条用例组装
    :param pr_id: 用例ID
    :return: 返回组装好的 testcase
    """
    testcase = json.loads(Testcases.objects.get(id=pr_id).request).get("test")
    # HttpRunner3.0 相关格式修改
    validates = []
    for i in range(len(testcase.get("validate"))):
        validate = {f'{testcase.get("validate")[i].get("comparator")}': [testcase.get("validate")[i].get("check"),
                                                                         testcase.get("validate")[i].get("expected")]}
        validates.append(validate)
    testcase["validate"] = validates
    return testcase


def run_testcase(testcase_dir, report_name):
    """
    利用HttpRunner执行用例并将相关数据存储到数据库
    :param report_name: 报告名称
    :param testcase_dir: 需要执行的目录
    :return: 返回生成 报告数据 ID
    """
    # 创建HttpRunner对象
    runner = HttpRunner()
    try:
        summary = runner.run(testcase_dir)
    except ParamsError:
        logger.error("用例参数有误")
        data = {
            "msg": "用例参数有误"
        }
        return Response(data, status=400)

    summary = timestamp_to_datetime(summary, type=False)
    report_id = create_report(summary, report_name)
    return Response({
        "id": report_id
    }, status=status.HTTP_201_CREATED)


def create_report(summary, report_name):
    """
    创建测试报告
    :param summary: runner 跑完的对象
    :param runner: HttpRunner对象
    :param report_name: 自定义报告名称
    :return:
    """
    # 定义报告名称并生成报告且获取报告内容
    report_path = report.gen_html_report(summary, report_template=r"stucit/template_new.html")

    # 继续格式化summary
    summary['time']['start_at'] = datetime. \
        fromtimestamp(int(summary['time']['start_at'])).strftime('%Y-%m-%d %H:%M:%S')
    summary['time']['duration'] = round(summary['time']['duration'], 2)
    for detail in summary['details']:
        detail['time']['duration'] = round(detail['time']['duration'], 2)
    # 处理前端所需数据
    case_list = []
    result_list = []
    case_details = []
    hasbeen = []
    i = 1
    for detail in summary.get("details"):
        if detail.get("records"):
            for record in detail.get("records"):
                case = {"value": i, "name": record.get("name")}
                if record.get("status") == "success":
                    name = "成功"
                elif record.get("status") == "error":
                    name = "失败"
                else:
                    name = "跳过"
                case_detail = {"result": record.get("status"), "case": i, "record": json.dumps(record)}
                i += 1
                case_list.append(case)
                case_details.append(case_detail)
                # 判断是否已经存在
                if not record.get("status") in hasbeen:
                    result = {"value": record.get("status"), "name": name}
                    result_list.append(result)
                hasbeen.append(record.get("status"))
    # 处理html文件中case中数据
    report_name_replacement = f'"{report_name}"'
    testResult = []
    for detail in summary["details"]:
        for record in detail["records"]:
            case = {
                "className": f'{record.get("name")}',
                "spendTime": f'{record.get("meta_datas").get("stat").get("elapsed_ms")}',
                "status": f'{record.get("status")}',
                "log": {
                    "url": f'{record.get("meta_datas").get("data")[0].get("request").get("url")}',
                    "method": f'{record.get("meta_datas").get("data")[0].get("request").get("method")}',
                    "status_code": f'{record.get("meta_datas").get("data")[0].get("response").get("status_code")}',
                    "request_headers": f'{record.get("meta_datas").get("data")[0].get("request").get("headers")}',
                    "request_body": f'{record.get("meta_datas").get("data")[0].get("request").get("body")}',
                    "response_headers": f'{record.get("meta_datas").get("data")[0].get("response").get("headers")}',
                    "response_body": f'{record.get("meta_datas").get("data")[0].get("response").get("body")}',
                    "conernt_type": f'{record.get("meta_datas").get("data")[0].get("response").get("content_type")}',
                    "error": f'{record.get("attachment")}',
                }
            }
            testResult.append(case)
    resulData_replacement = {
        "testPass": summary.get("stat").get("teststeps").get("successes"),
        "testAll": summary.get("stat").get("teststeps").get("total"),
        "testFail": summary.get("stat").get("teststeps").get("errors"),
        "testSkip": summary.get("stat").get("teststeps").get("skipped"),
        "beginTime": summary.get("time").get("start_at"),
        "totalTime": summary.get("time").get("duration"),
        "testName": f'"{report_name}"',
        "testResult": testResult

    }
    with open(report_path, encoding='utf-8') as stream:
        reports = stream.read().replace("report_name_replacement", report_name_replacement).replace(
            "resulData_replacement", json.dumps(resulData_replacement))
    os.remove(report_path)

    test_report = {
        'name': report_name + "_" + datetime.strftime(datetime.now(), '%Y%m%d%H%M%S'),
        'result': summary.get('success'),
        'success': summary.get('stat').get('teststeps').get("successes"),
        'filed': summary.get('stat').get('teststeps').get("errors"),
        'skip': summary.get('stat').get('teststeps').get("skipped"),
        'count': summary.get('stat').get('teststeps').get("total"),
        'html': reports,
        'summary': json.dumps(summary),
        "case_list": case_list,
        "result_list": result_list,
        "case_details": case_details
    }

    report_obj = ReportsModel.objects.create(**test_report)
    return report_obj.id


def timestamp_to_datetime(summary, type=True):
    """
    summy数据格式化
    :param summary:
    :param type:
    :return:
    """
    if not type:
        time_stamp = int(summary["time"]["start_at"])
        summary['time']['start_datetime'] = datetime. \
            fromtimestamp(time_stamp).strftime('%Y-%m-%d %H:%M:%S')

    for detail in summary['details']:
        try:
            time_stamp = int(detail['time']['start_at'])
            detail['time']['start_at'] = datetime.fromtimestamp(time_stamp).strftime('%Y-%m-%d %H:%M:%S')
        except Exception:
            pass
    return summary
