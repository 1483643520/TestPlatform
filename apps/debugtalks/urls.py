#!/user/bin/even Python3
# -*- coding:utf-8 -*-
# urls.py.py
# 子路由函数
# author:zhaohexin
# time：2019/12/10 10:02 下午


from django.urls import path
from django.urls import path
from rest_framework import routers

from .views import DebugtalksViewSet

# 创建路由集
router = routers.SimpleRouter()
# 确定前缀
router.register(r"debugtalks", DebugtalksViewSet)

urlpatterns = [
]

# 生成路由信息
urlpatterns += router.urls
