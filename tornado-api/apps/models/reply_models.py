from datetime import datetime

from peewee import *

from blog.models import BaseModel
from apps.utils.utils import get_md5

from .comment_models import CommentInfoModel


class ReplyInfoModel(BaseModel):
    portrait = CharField(verbose_name="回复者用户头像", max_length=1000)
    name = CharField(verbose_name="回复者用户名", max_length=100)
    email = CharField(verbose_name="回复者用户邮箱", max_length=100)
    site = CharField(verbose_name="回复者网站", max_length=1000)
    ip = CharField(max_length=100, verbose_name="用户IP")
    lin_lat = CharField(max_length=100, null=True, verbose_name='经纬度')
    city = CharField(max_length=30, verbose_name="用户所在城市")
    province = CharField(max_length=100, null=True, verbose_name='省份')
    country = CharField(max_length=100)
    agent = CharField(max_length=200, verbose_name="用户UA")
    uuid = CharField(verbose_name='回复者信息ID', max_length=50, default=get_md5)


class ReplyCommentInfoModel(BaseModel):
    portrait = CharField(verbose_name="回复者用户头像", max_length=1000)
    name = CharField(verbose_name="回复者用户名", max_length=100)
    email = CharField(verbose_name="回复者用户邮箱", max_length=100)
    site = CharField(verbose_name="回复者网站", max_length=1000)
    ip = CharField(max_length=100, verbose_name="用户IP")
    lin_lat = CharField(max_length=100, null=True, verbose_name='经纬度')
    city = CharField(max_length=30, verbose_name="用户所在城市")
    province = CharField(max_length=100, null=True, verbose_name='省份')
    country = CharField(max_length=100)
    agent = CharField(max_length=200, verbose_name="用户UA")
    uuid = CharField(verbose_name='回复评论者信息ID', max_length=50, default=get_md5)


class ReplyModel(BaseModel):
    article_id = CharField(verbose_name="评论所在文章ID", max_length=100)
    uuid = CharField(verbose_name='回复ID', max_length=50, default=get_md5)
    cid = CharField(verbose_name='评论ID', max_length=50)

    com_info = ForeignKeyField(CommentInfoModel, verbose_name='评论者信息')
    reply_info = ForeignKeyField(ReplyInfoModel, verbose_name='回复者信息')
    reply_comment = ForeignKeyField(ReplyCommentInfoModel, verbose_name="回复评论者的信息")

    content = TextField(verbose_name="回复者评论内容")
    likes = IntegerField(verbose_name="回复者评论喜欢数", default=0)

    is_comment = CharField(max_length=10, default='reply')

    state = IntegerField(choices=((0, "待审核"), (1, "通过"), (2, "不通过")), default=1)
    update_time = DateTimeField(default=datetime.now, verbose_name="更新时间")

    @classmethod
    def extend(cls):
        return cls.select(cls, CommentInfoModel, ReplyInfoModel, ReplyCommentInfoModel).join(
            CommentInfoModel, on=cls.com_info).switch(cls).join(
            ReplyInfoModel, on=cls.reply_info).switch(cls).join(
            ReplyCommentInfoModel, on=cls.reply_comment
        )
