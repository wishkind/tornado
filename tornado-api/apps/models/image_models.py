from peewee import *
from datetime import datetime

from blog.models import BaseModel

from apps.utils.utils import get_md5


class ImageModel(BaseModel):
    image_name = CharField(max_length=100, verbose_name='图片名称')
    url_path = CharField(max_length=1000, null=True, verbose_name='图片链接')
    tag = CharField(max_length=50, verbose_name='标签')
    uuid = CharField(max_length=100, default=get_md5, verbose_name='图片唯一ID')
    update_time = DateTimeField(default=datetime.now, verbose_name="更新时间")

