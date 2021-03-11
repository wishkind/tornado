from peewee import *

from blog.models import BaseModel


class PublicModel(BaseModel):
    article_count = IntegerField(verbose_name='文章总数')
