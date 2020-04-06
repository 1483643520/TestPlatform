import datetime

from django.db.models import Count, Sum

from debugtalks.models import DebugTalksModel
from interfaces.models import Interfaces
from projects.models import Projects
from reports.models import ReportsModel
from testcase.models import Testcases
from testsuits.models import Testsuits


def cartogram_one():
    """
    组装统计图表1数据
    :return:
    """

    year_now = datetime.datetime.now().strftime('%Y')
    # 按当前年以月份分组进行计算数量
    projects_count_month = Projects.objects.values("create_time__month").annotate(configures=Count("id")).filter(
        create_time__year=year_now)
    projects_count_data = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for item in projects_count_month:
        projects_count_data[item["create_time__month"] - 1] += item["configures"]
    interface_count_month = Interfaces.objects.values("create_time__month").annotate(configures=Count("id")).filter(
        create_time__year=year_now)
    interfaces_count_data = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for item in interface_count_month:
        interfaces_count_data[item["create_time__month"] - 1] += item["configures"]
    testsuits_count_month = Testsuits.objects.values("create_time__month").annotate(configures=Count("id")).filter(
        create_time__year=year_now)
    testsuits_count_data = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for item in testsuits_count_month:
        testsuits_count_data[item["create_time__month"] - 1] += item["configures"]
    testcases_count_month = Testcases.objects.values("create_time__month").annotate(configures=Count("id")).filter(
        create_time__year=year_now)
    testcases_count_data = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for item in testcases_count_month:
        testcases_count_data[item["create_time__month"] - 1] += item["configures"]
    reports_count_month = ReportsModel.objects.values("create_time__month").annotate(configures=Count("id")).filter(
        create_time__year=year_now)
    reports_count_data = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for item in reports_count_month:
        reports_count_data[item["create_time__month"] - 1] += item["configures"]
    debugtalks_count_month = DebugTalksModel.objects.values("create_time__month").annotate(
        configures=Count("id")).filter(create_time__year=year_now)
    debugtalks_count_data = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for item in debugtalks_count_month:
        debugtalks_count_data[item["create_time__month"] - 1] += item["configures"]
    # 组装数据并返回
    option_one = {
        "year_now": year_now,
        "series": [
            {
                "name": '项目数量',
                "type": 'bar',
                "data": projects_count_data,
                "markLine": {
                    "lineStyle": {
                        "type": 'dashed'
                    },
                    "data": [
                        [{"type": 'min'}, {"type": 'max'}]
                    ]
                }
            },
            {
                "name": '接口数量',
                "type": 'bar',
                "data": interfaces_count_data,
                "markLine": {
                    "lineStyle": {
                        "type": 'dashed'
                    },
                    "data": [
                        [{"type": 'min'}, {"type": 'max'}]
                    ]
                }
            },
            {
                "name": '套件数量',
                "type": 'bar',
                "data": testsuits_count_data,
                "markLine": {
                    "lineStyle": {
                        "type": 'dashed'
                    },
                    "data": [
                        [{"type": 'min'}, {"type": 'max'}]
                    ]
                }
            },
            {
                "name": '用例数量',
                "type": 'bar',
                "data": testcases_count_data,
                "markLine": {
                    "lineStyle": {
                        "type": 'dashed'
                    },
                    "data": [
                        [{"type": 'min'}, {"type": 'max'}]
                    ]
                }
            },
            {
                "name": '报告数量',
                "type": 'bar',
                "data": reports_count_data,
                "markLine": {
                    "lineStyle": {
                        "type": 'dashed'
                    },
                    "data": [
                        [{"type": 'min'}, {"type": 'max'}]
                    ]
                }
            },
            {
                "name": '函数文件数量',
                "type": 'bar',
                "data": debugtalks_count_data,
                "markLine": {
                    "lineStyle": {
                        "type": 'dashed'
                    },
                    "data": [
                        [{"type": 'min'}, {"type": 'max'}]
                    ]
                }
            },
        ]
    }
    return option_one


def cartogram_two():
    """
    执行结果地图数据组装
    :return:
    """
    year_now = datetime.datetime.now().strftime('%Y')
    success_count_data = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    field_count_data = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    skip_count_data = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    success_count_month = ReportsModel.objects.values("create_time__month").annotate(Sum("success")).filter(
        create_time__year=year_now)
    for item in success_count_month:
        success_count_data[item["create_time__month"] - 1] += item["success__sum"]
    filed_count_month = ReportsModel.objects.values("create_time__month").annotate(Sum("filed")).filter(
        create_time__year=year_now)
    for item in filed_count_month:
        field_count_data[item["create_time__month"] - 1] += item["filed__sum"]
    skip_count_month = ReportsModel.objects.values("create_time__month").annotate(Sum("skip")).filter(
        create_time__year=year_now)
    for item in skip_count_month:
        skip_count_data[item["create_time__month"] - 1] += item["skip__sum"]
    option = {
        "year_now": year_now,
        "series": [
            {
                "name": '成功',
                "type": 'bar',
                "data": success_count_data,
                "markPoint": {
                    "data": [
                        {"type": 'max', "name": '最大值'},
                        {"type": 'min', "name": '最小值'}
                    ]
                },
                "markLine": {
                    "data": [
                        {"type": 'average', "name": '平均值'}
                    ]
                }
            },
            {
                "name": '失败',
                "type": 'bar',
                "data": field_count_data,
                "markPoint": {
                    "data": [
                        {"type": 'max', "name": '最大值'},
                        {"type": 'min', "name": '最小值'}
                    ]
                },
                "markLine": {
                    "data": [
                        {"type": 'average', "name": '平均值'}
                    ]
                }
            },
            {
                "name": '跳过',
                "type": 'bar',
                "data": skip_count_data,
                "markPoint": {
                    "data": [
                        {"type": 'max', "name": '最大值'},
                        {"type": 'min', "name": '最小值'}
                    ]
                },
                "markLine": {
                    "data": [
                        {"type": 'average', "name": '平均值'}
                    ]
                }
            },

        ]

    }
    return option
