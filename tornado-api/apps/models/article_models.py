from datetime import datetime

from peewee import *

from apps.utils.utils import get_md5
from blog.models import BaseModel

from .tag_models import TagModel


class ArticleModel(BaseModel):
    title = CharField(max_length=100, index=True, verbose_name='文章标题')
    uuid = CharField(max_length=100, default=get_md5, verbose_name='文章ID')
    keyword = CharField(max_length=100, verbose_name='关键字', null=True)
    desc = CharField(max_length=300, verbose_name='描述-简介', null=True)
    tag = CharField(max_length=100, verbose_name="标签", null=True)
    content = TextField(verbose_name='文章内容', null=True)
    edit_content = TextField(verbose_name='编辑内容', default=content, null=True)
    state = IntegerField(choices=(
        (1, "发布"), (2, "草稿")
    ), verbose_name="状态", default=1)
    views = IntegerField(verbose_name="观看数", default=0)
    likes = IntegerField(verbose_name="喜欢数", default=0)
    comments = IntegerField(verbose_name="评论数", default=0)
    publish = IntegerField(choices=((1, "公开"), (2, "私密")), verbose_name="文章公开状态", default=1)
    thumb = CharField(verbose_name="缩略图", max_length=1000, null=True)
    type = IntegerField(choices=((1, "code"), (2, "think"), (3, "民谣")), verbose_name="文章分类", default=1)
    update_time = DateTimeField(default=datetime.now, verbose_name="更新时间")

    @classmethod
    def extends(cls):
        return cls.select(cls).join(TagModel, on=(cls.uuid, TagModel.uuid))

