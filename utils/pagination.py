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
    max_page_size = 20
    # 配置每页展示数据量 - 默认值
    page_size = 10
    # 覆盖指认每页最大数据key
    page_size_query_param = 'size'
    # 重置提示信息
    page_query_description = "第几页"
    page_size_query_description = "每页条数"

    def get_paginated_response(self, data):
        """
        从写分页返回方法，实现返回值新增当前页/总页数操作
        :param data:
        :return:
        """
        response = super().get_paginated_response(data)
        # 新增当前页/总页数
        response.data["current_page_num"] = self.page.number
        response.data["total_pages"] = self.page.paginator.num_pages
        return response
