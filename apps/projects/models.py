from django.db import models
from utils.base_model import BaseModel

# Create your models here.
# 迁移数据模型
# 执行命令
# python manage.py makemigrations 子应用名
# 更加完整的命令：python manage.py makemigrations --empty projects
# python manage.py migrate 子应用名
# 也可以用专业版 tools run manage.py Task..
# makemigrations 子应用名
# migrate 子应用名


"""
1、每个应用下的数据库模型类，需要在当前应用系 projects/models.py 文件中定义
2、一个数据库模型类相当于一个数据表（table）
3、数据库模型类必须继承models.Model或者models.Model子类
4、模型类中定义的类属性，相当于数据表中的一个类字段
5、默认会创建一个自动递增的id主键
"""


class Projects(BaseModel):
    """
    创建Projects数据库模型类
    """
    # 创建自增id组件 models.AutoField
    # 如果手动创建了一个primary_key = True的类属性，Django就不会自动创建
    # verbose_name="id主键" 可以设置更人性化的字段名
    # help_text = "id主键" 可以设置字段的描述信息（在api接口文档）
    id = models.AutoField(verbose_name="id主键", primary_key=True, help_text="id主键")
    # 创建字符串类型字段
    # unique = True 设置当前字段是否为唯一，默认为False
    # max_length = 300 设置当前字段最大字节
    # default = "" 设置默认值
    # blank = True blank用于设置在创建项目时前端可以不用传此字段
    # null = True 用于设置数据库此字段允许为空
    name = models.CharField(verbose_name="项目名称", help_text="项目名称", unique=True, max_length=255)
    leader = models.CharField(verbose_name="项目负责人", help_text="项目负责人", max_length=50)
    tester = models.CharField(verbose_name="测试人员", help_text="测试人员", max_length=50)
    programmer = models.CharField(verbose_name="开放人员", help_text="开放人员", max_length=50)
    publish_app = models.CharField(verbose_name="发布应用", help_text="发布应用", max_length=100)
    desc = models.CharField(verbose_name="项目描述", help_text="项目描述", max_length=100, default="", blank=True,
                            null=True)

    # 默认情况下创建的表名为：子应用名_模型类名小写
    # 创建内部类，修改数据库表名
    class Meta:
        """
        定义Meta内部类，用于设置当前数据模型元数据信息，必须是Meta类
        """
        # 重新指认数据表名
        db_table = "tb_projects"
        # 指认数据表描述
        verbose_name = "项目表"

    def __str__(self):
        return self.name
