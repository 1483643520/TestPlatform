from django.db import models
from utils.base_model import BaseModel


# Create your models here.


class DebugTalksModel(BaseModel):
    """
    内置函数模型类
    """
    id = models.AutoField(verbose_name="主键", primary_key=True, help_text="id主键")
    name = models.CharField(verbose_name="debugtalk文件名称", max_length=200, default="debugtalk.py",
                            help_text="debugtalk文件名称")
    debugtalk = models.TextField(null=True, default="#debugtalk.py", help_text="debugtalk.py文件内容")
    project = models.OneToOneField("projects.Projects", on_delete=models.CASCADE, related_name="debugtalks",
                                   help_text="所属")

    class Meta:
        db_table = "tb_debugtalks"
        verbose_name = "debugtalk.py文件"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
