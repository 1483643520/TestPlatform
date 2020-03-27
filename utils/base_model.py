#!/user/bin/even Python3
# -*- coding:utf-8 -*-
# base_model.py
# 公共数据库模型字段
# author:zhaohexin
# time：2020/2/19 9:11 上午

from django.db import models


class BaseModel(models.Model):
    """
    创建公共字段类
    """
    create_time = models.DateTimeField(auto_now_add = True, verbose_name = "创建时间", help_text = "创建时间")
    update_time = models.DateTimeField(auto_now = True, verbose_name = "更新时间", help_text = "更新时间")
    
    # 默认情况下创建的表名为：子应用名_模型类名小写
    # 创建内部类，修改数据库表名
    class Meta:
        """
        定义Meta内部类，用于设置当前数据模型元数据信息，必须是Meta类
        """
        # 指定为抽象模型类，在迁移时，不会自动创建table表
        abstract = True
        verbose_name = "公共字段"
