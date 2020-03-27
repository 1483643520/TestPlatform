from django.db import models
from utils.base_model import BaseModel

# Create your models here.

class Interfaces(BaseModel):
    """
    接口类型模型库
    一个接口往往属于一个项目
    项目表和接口表的关系：一对多，需要在多地一侧去创建外键
    """
    # 创建自增id组件 models.AutoField
    # 如果手动创建了一个primary_key = True的类属性，Django就不会自动创建
    # verbose_name="id主键" 可以设置更人性化的字段名
    # help_text = "id主键" 可以设置字段的描述信息（在api接口文档）
    id = models.AutoField(verbose_name = "id主键", primary_key = True, help_text = "id主键")
    # 创建字符串类型字段
    # unique = True 设置当前字段是否为唯一，默认为False
    # max_length = 300 设置当前字段最大字节
    # default = "" 设置默认值
    # blank = True blank用于设置在创建项目时前端可以不用传此字段
    # null = True 用于设置数据库此字段允许为空
    name = models.CharField(verbose_name = "接口名称", help_text = "接口名称", unique = True, max_length = 255)
    tester = models.CharField(verbose_name = "测试人员", help_text = "测试人员", max_length = 50)
    desc = models.CharField(verbose_name = "接口描述", help_text = "接口描述", max_length = 100, default = "", blank = True,
                            null = True)
    # 创建外键字段
    # 第一个参数为指向主表（应用名.模型类）
    # on_delete设置的是，当父表（项目表）中的数据删除之后，从表字段的处理方式--models.CASCADE():当主要删除时，子表数据同时删除
    # models.SET_NULL 字表会自动设置为NULL
    # related_name指定父表对字表引用名，如不指定，默认为子表模型类小写_set
    project = models.ForeignKey("projects.Projects", on_delete = models.CASCADE, related_name = "interfaces",
                                help_text = "所属项目", verbose_name = "所属项目")
    
    class Meta:
        db_table = "tb_interfaces"
        verbose_name = "接口表"
    
    def __str__(self):
        return self.name
