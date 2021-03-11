from datetime import datetime
from peewee import *

from apps.utils.utils import get_md5
from blog.models import BaseModel


class ProjectModel(BaseModel):
    uuid = CharField(max_length=20, default=get_md5)
    title = TextField(verbose_name="标题")
    desc = TextField(verbose_name="描述")
    icon = CharField(verbose_name="icon图")
    github = CharField(verbose_name="项目git链接")
    view = CharField(verbose_name="预览地址")
    state = IntegerField(choices=((1, "通过"), (2, "待审核")), verbose_name="项目状态", default=1)
    update_time = DateTimeField(default=datetime.now, verbose_name="更新日期")
