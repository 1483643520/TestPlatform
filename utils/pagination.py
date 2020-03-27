#!/user/bin/even Python3
# -*- coding:utf-8 -*-
# pagination.py
# 自定义分页
# author:zhaohexin
# time：2020/1/1 5:49 下午

from rest_framework.pagination import PageNumberPagination

class ManualPageNumberPagination(PageNumberPagination):
    """
    自定义分页类
    """
    # 覆盖前端参数key
    # page_query_param = "q"
    # 配置 前端可以指定每页最大数据 - 默认值
    max_page_size = 5
    # 配置每页展示数据量 - 默认值
    page_size = 5
    # 覆盖指认每页最大数据key
    # page_size_query_param = "s"
