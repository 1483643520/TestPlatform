from django.db import models
from utils.base_model import BaseModel
from django.conf import settings


# Create your models here.


class BacklogModel(BaseModel):
    """
    全局配置信息数据库模型
    """
    id = models.AutoField(verbose_name="主键", primary_key=True, help_text="id主键")
    text = models.TextField(verbose_name="待办事项详情", help_text="待办事项详情")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                             related_name="user_id", help_text="所属用户id")
    status = models.BooleanField(verbose_name="完成状态", help_text="完成状态", default=0)

    class Meta:
        db_table = "tb_backlog"
        verbose_name = "待办事项信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
