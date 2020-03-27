import json

from django.http import JsonResponse

# Create your views here.
from django.views import View
from interfaces import models


def return_information(data, status = 200, msg = "成功"):
    """
    根据状态码，返回不同的json信息
    @param msg: 返回提示信息，默认为成功
    @param data: 数据信息
    @param status: 状态码，默认200
    @return: 组装好的json文件
    """
    json_ = {
        "status": status,
        "msg": msg,
        "data": data
    }
    return json_


class Interfaces(View):
    """
    获取所有端口信息或更新接口信息
    """
    
    def get(self, request):
        """
        获取所有接口信息
        @param request:
        @return:
        """
        # 获取信息并编辑成列表,并进行排序
        interfaces = [i for i in models.Interfaces.objects.filter().values().order_by("project__id", "id")]
        # 组装返回参数
        json_ = return_information(interfaces, 200, "查询成功！")
        # 返回参数
        return JsonResponse(json_, json_dumps_params = {'ensure_ascii': False})
    
    def post(self, request):
        """
        创建接口信息
        @param request:
        @return:
        """
        # 获取新增参数
        datas = request.body
        # 反序列化 -- 转换为json格式
        datas_ = json.loads(datas, encoding = 'utf-8')
        # TODO:待添加 解析校验参数
        # 组装新增项
        create_ = {"name": datas_["name"], "tester": datas_["tester"], "desc": datas_["desc"],
                   "project_id": datas_["project_id"]}
        # 新增数据
        models.Interfaces.objects.create(**create_)
        # 获取新增数据
        create_data = [i for i in models.Interfaces.objects.filter(**create_).values()]
        # 合成返回数据
        json_ = return_information(create_data, 201, "新增成功！")
        # 返回新增的数据
        return JsonResponse(json_, json_dumps_params = {'ensure_ascii': False})


class InterfacesEdit(View):
    """
    接口信息的编辑及单条获取
    """
    
    def get(self, request, pk):
        """
        获取某一条接口的值
        @param request:
        @param pk:获取接口id
        @return:
        """
        # 获取数据
        data = [i for i in models.Interfaces.objects.filter(id = pk).values()]
        # 组装数据
        json_ = return_information(data, 200, "查询成功！")
        # 返回数据
        return JsonResponse(json_, json_dumps_params = {'ensure_ascii': False})
    
    def put(self, request, pk):
        """
        修改某条接口的全部信息
        @param pk: url路径参数，接收需要修改的接口id
        @param request:
        @return:
        """
        # 获取新增参数
        datas = request.body
        # 反序列化 -- 转换为json格式
        datas_ = json.loads(datas, encoding = 'utf-8')
        # TODO:待添加 解析校验参数
        # 组装新增项
        update_ = {"name": datas_["name"], "tester": datas_["tester"], "desc": datas_["desc"]}
        # TODO: 一堆乱七八糟的校验
        # 获取需要修改的全部数据并更新字段[批量，查询时只能用filter，且自动保存]
        models.Interfaces.objects.filter(id = pk).update(**update_)
        # 查询更新后的值
        update_data = [i for i in models.Interfaces.objects.filter(id = pk).values()]
        # 组装返回数据
        json_ = return_information(update_data, 201, "修改数据成功")
        return JsonResponse(json_, json_dumps_params = {'ensure_ascii': False})
    
    def delete(self, request, pk):
        """
        删除某条接口
        @param pk:
        @param request:
        @return:
        """
        # TODO:各种数据校验
        # 删除数据
        models.Interfaces.objects.get(id = pk).delete()
        # 整合返回数据
        json_ = return_information([], 204, "删除成功")
        return JsonResponse(json_, json_dumps_params = {'ensure_ascii': False})


class InterfacesForProjects(View):
    """
    根据项目来查询接口
    """
    
    def get(self, request, pk):
        """
        根据项目编码，查询接口信息
        @param request:
        @param pk: 项目编码
        @return:
        """
        # TODO:一大堆乱七八糟校验
        # 获取数据
        data = [i for i in models.Interfaces.objects.filter(project_id = pk).values()]
        # 组装数据
        json_ = return_information(data, 200, "查询成功！")
        # 返回数据
        return JsonResponse(json_, json_dumps_params = {'ensure_ascii': False})

# TODO:待做部分字段更新
