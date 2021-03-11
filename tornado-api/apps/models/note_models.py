from datetime import datetime
from peewee import *

from apps.utils.utils import get_md5
from blog.models import BaseModel


class NoteModel(BaseModel):
    uuid = CharField(max_length=20, default=get_md5)
    name = TextField(verbose_name="网站名称")
    desc = TextField(verbose_name="网站描述", null=True)
    logo = CharField(verbose_name="网站logo", null=True)
    link = CharField(verbose_name="网站链接")
    state = IntegerField(choices=((1, "通过"), (2, "待审核")), verbose_name="项目状态", default=2)
    update_time = DateTimeField(default=datetime.now, verbose_name="更新日期")
