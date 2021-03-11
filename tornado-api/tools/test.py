import re

from peewee import *
import datetime
import uuid
from playhouse.shortcuts import model_to_dict

db = MySQLDatabase("test", host="127.0.0.1", port=3306, user="root", passwd="5211314")
db.connect()


class BaseModel(Model):
    class Meta:
        database = db


class Info(BaseModel): # , to_field=Tag.name, backref='tags'
    name = CharField(max_length=100)
    email = CharField(max_length=100)
    uuid = CharField(default=uuid.uuid1, max_length=100)
    create_time = DateTimeField(default=datetime.datetime)


class Comment(BaseModel):
    content = CharField(max_length=100)
    info = ForeignKeyField(Info)
    uuid = CharField(default=uuid.uuid1, max_length=100)


def test():
    i = Info.select(Info).dicts()
    print(i)
    for a in i:
        print(a)
    # c = Comment.get(Comment.content=='aaaaa')
    # print(model_to_dict(c))
    # u = Article.select().where(Article.id==2)
    # for a in u:
    #     print(model_to_dict(a))


def test_ip():
    remote_ip = '172.17.0.1'
    remote_ip = '192.168.10.31'
    ip = re.findall('^(127\\.0\\.0\\.1)|(localhost)|(10\\.\\d{1,3}\\.\\d{1,3}\\.\\d{1,3})|(172\\.((1[6-9])|(2\\d)|(3[01]))\\.\\d{1,3}\\.\\d{1,3})|(192\\.168\\.\\d{1,3}\\.\\d{1,3})$', remote_ip)

    # rex_ip = re.compile(
    #     '^(127\\.0\\.0\\.1)|(localhost)|(10\\.\\d{1,3}\\.\\d{1,3}\\.\\d{1,3})|(172\\.((1[6-9])|(2\\d)|(3[01]))\\.\\d{1,3}\\.\\d{1,3})|(192\\.168\\.\\d{1,3}\\.\\d{1,3})$')

    if ip:
        print('1111111')


if __name__ == "__main__":
    # 创建表
    test_ip()
    # db.create_tables([Info, Comment])
    # Tag.create_table()  # 创建User表
    # Article.create_table()  # 创建Tweet表
