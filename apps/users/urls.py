#!/user/bin/even Python3
# -*- coding:utf-8 -*-
# urls.py
# 用户路由信息
# author:zhaohexin
# time：2020/1/8 11:10 下午
from django.urls import path, re_path
from rest_framework import routers

from .views import UsersViewSet, UsernameValidateView, EmailValidateView
from rest_framework_jwt.views import obtain_jwt_token

# 创建路由集
router = routers.DefaultRouter()
# 确定前缀
router.register(r"register", UsersViewSet)

urlpatterns = [
    # 调用jwt默认登录返回token信息
    path("login/", obtain_jwt_token),
    re_path(r'^(?P<username>\w{6,20})/count/$', UsernameValidateView.as_view(), name="check_username"),
    re_path(r'^(?P<email>[A-Za-z0-9]+@[A-Za-z0-9]+\.[A-Za-z0-9_-]+)/count/$', EmailValidateView.as_view(), name="check_email"),

]

# 生成路由信息
urlpatterns += router.urls
