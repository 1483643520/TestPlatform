#!/user/bin/even Python3
# -*- coding:utf-8 -*-
# urls.py
# 用户路由信息
# author:zhaohexin
# time：2020/1/8 11:10 下午
from django.urls import path
from rest_framework import routers

from .views import UsersViewSet, Check
from rest_framework_jwt.views import obtain_jwt_token

# 创建路由集
router = routers.DefaultRouter()
# 确定前缀
router.register(r"users", UsersViewSet)

urlpatterns = [
    # 调用jwt默认登录返回token信息
    path("login/", obtain_jwt_token),
    path("users/<pk>/count/", Check.as_view())
]

# 生成路由信息
urlpatterns += router.urls
