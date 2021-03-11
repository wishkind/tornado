from datetime import datetime
from peewee import *

from apps.utils.utils import get_md5
from blog.models import BaseModel


class HeroInfoModels(BaseModel):
    name = CharField(max_length=100, verbose_name="姓名")

    portrait = CharField(verbose_name="用户头像", max_length=1000)
    email = CharField(max_length=100, verbose_name="邮箱")
    site = CharField(verbose_name="网站", max_length=200)
    agent = CharField(max_length=1000, verbose_name="用户UA")

    city = CharField(max_length=100)
    province = CharField(max_length=100, verbose_name='省份')
    country = CharField(max_length=100)
    uuid = CharField(max_length=20, default=get_md5)


class HeroModels(BaseModel):
    uuid = CharField(max_length=20, default=get_md5)
    hero_info = ForeignKeyField(HeroInfoModels)
    content = TextField(verbose_name="内容")
    state = IntegerField(choices=((0, "待审核"), (1, "通过"), (2, "不通过")), verbose_name="评论状态", default=1)
    reply = IntegerField(verbose_name="评论数", default=0)
    update_time = DateTimeField(default=datetime.now, verbose_name="更新日期")

    @classmethod
    def extends(cls):
        return cls.select(cls, HeroInfoModels).join(HeroInfoModels)
