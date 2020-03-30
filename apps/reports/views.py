# Create your views here.
import json
import os

from django.conf import settings
from django.http import StreamingHttpResponse
from django.utils.encoding import escape_uri_path
from rest_framework.response import Response
from rest_framework import viewsets, permissions
from rest_framework import mixins
from rest_framework.decorators import action

from . import models
from . import serializers
from . import utils
from .utils import get_file_content


class ReportsViewSet(viewsets.GenericViewSet, mixins.DestroyModelMixin, mixins.ListModelMixin,
                     mixins.RetrieveModelMixin):
    """

    list:
    获取结果集

    retrieve:
    获取具体一条接口信息

    destroy：
    删除接口

    """

    # 定义 queryset 查询集
    queryset = models.ReportsModel.objects.all()
    # 定义 serializer_class 序列化器类
    serializer_class = serializers.ReportsSerializer
    """
    # 定义过滤引擎，排序引擎，分页引擎,也可以在setting中设置默认项,此项目在setting中配置，一下为类中配置
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    pagination_class = [PageNumberPagination]
    """
    # 定义筛选字段
    filterset_fields = ["id", "name"]
    # 定义排序字段
    ordering_fields = ["id", "name"]
    # 登录才能操作
    permission_classes = [permissions.IsAuthenticated]

    # 从新定义list查询
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        response.data["results"] = utils.format_output(response.data["results"])
        return response

    # def retrieve(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance)
    #     datas = serializer.data
    #     try:
    #         datas['summary'] = json.loads(datas['summary'], encoding='utf-8')
    #     except Exception as e:
    #         pass
    #     return Response(datas)

    @action(methods=["get"], detail=True)
    def download(self, *args, **kwargs):
        # 1. 手动创建报告
        instance = self.get_object()
        html = instance.html

        report_path = settings.REPORTS_DIR
        report_full_path = os.path.join(report_path, instance.name) + '.html'
        with open(report_full_path, 'w', encoding='utf-8') as file:
            file.write(html)

        # 2. 读取创建的报告并返回给前端
        # 如果要提供前端用户能够下载文件, 那么需要在响应头中添加如下字段:
        # Content-Type = application/octet-stream
        # Content-Disposition = attachment; filename*=UTF-8'' 文件名
        response = StreamingHttpResponse(get_file_content(report_full_path))
        # 对文件名进行转义
        report_path_final = escape_uri_path(instance.name + '.html')
        # StreamingHttpResponse对象类似于dict字典
        # 如果以字典的形式添加key-value, 那么添加的是响应头信息
        response['Content-Type'] = 'application/octet-stream'
        response["Content-Disposition"] = "attachment; filename*=UTF-8''{}".format(report_path_final)

        return response

