from django.db import models
from utils.base_model import BaseModel


# Create your models here.


class Configures(BaseModel):
    """
    全局配置信息数据库模型
    """
    id = models.AutoField(verbose_name = "主键", primary_key = True, help_text = "id主键")
    name = models.CharField(verbose_name = "配置名称", max_length = 50, help_text = "配置名称")
    interface = models.ForeignKey("interfaces.Interfaces", on_delete = models.CASCADE,
                                  related_name = "configures", help_text = "所属接口")
    author = models.CharField(verbose_name = "编写人员", max_length = 50, help_text = "编写人员")
    request = models.TextField(verbose_name = "请求信息", help_text = "请求信息")
    
    class Meta:
        db_table = "tb_configures"
        verbose_name = "配置信息"
        verbose_name_plural = verbose_name
    
    def __str__(self):
        return self.name
