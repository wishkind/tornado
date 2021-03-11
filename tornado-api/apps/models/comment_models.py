from datetime import datetime

from peewee import *

from blog.models import BaseModel
from apps.utils.utils import get_md5
from apps.models.article_models import ArticleModel


class CommentInfoModel(BaseModel):
    ip = CharField(max_length=30, verbose_name="IP地址")
    city = CharField(max_length=100, null=True, verbose_name='城市')
    province = CharField(max_length=100, null=True, verbose_name='省份')
    country = CharField(max_length=100, null=True, verbose_name='国家')
    lin_lat = CharField(max_length=100, null=True, verbose_name='经纬度')
    agent = CharField(max_length=500, verbose_name="用户UA")
    portrait = CharField(verbose_name="用户头像", max_length=1000)
    name = CharField(max_length=100, verbose_name="用户名")
    email = CharField(max_length=100, verbose_name="邮箱")
    site = CharField(verbose_name="网站", max_length=100)
    uuid = CharField(verbose_name="评论者信息ID", default=get_md5, max_length=50)


class CommentModel(BaseModel):
    article = ForeignKeyField(ArticleModel, verbose_name='文章信息')
    uuid = CharField(verbose_name="评论ID", default=get_md5, max_length=50)
    content = TextField(verbose_name="评论内容")
    likes = IntegerField(verbose_name="评论被赞数", default=0)
    comment_info = ForeignKeyField(CommentInfoModel, verbose_name='评论个人信息')
    state = IntegerField(choices=((0, "待审核"), (1, "通过"), (2, "不通过")), verbose_name="评论状态", default=1)
    reply = IntegerField(verbose_name="回复评论数", default=0)
    update_time = DateTimeField(default=datetime.now, verbose_name="更新日期")

    @classmethod
    def extend(cls):
        return cls.select(cls, CommentInfoModel, ArticleModel).join(
            CommentInfoModel, on=cls.comment_info).switch(cls).join(
            ArticleModel, on=cls.article
        )
