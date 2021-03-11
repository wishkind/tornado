from datetime import datetime

from peewee import *

from apps.utils.utils import get_md5
from blog.models import BaseModel


class TagModel(BaseModel):
    name = CharField(verbose_name="标签名称", max_length=100, primary_key=True)
    desc = CharField(verbose_name="标签描述", max_length=300)
    uuid = CharField(max_length=100, default=get_md5, verbose_name='标签ID')
    ta_count = IntegerField(verbose_name='标签对应的文章数', default=0)
    update_time = DateTimeField(default=datetime.now, verbose_name="更新时间")
