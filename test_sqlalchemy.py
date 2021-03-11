# -*- coding:utf-8 -*-
import pymysql.connections
import pymysql.converters
import pymysql.cursors
pymysql.install_as_MySQLdb()
import MySQLdb
from datetime import datetime

from sqlalchemy import (Table, MetaData, create_engine,
                        Column, Integer, String, SmallInteger, DateTime)
from sqlalchemy.orm import mapper, sessionmaker

engine = create_engine("mysql+mysqldb://root:dragon@127.0.0.1/deng?charset=utf8")
metadata = MetaData()


class BaseModel(object):

    create_time = Column(DateTime, default=datetime.now)  
    update_time = Column(DateTime, default=datetime.now, onupdate=datetime.now)  

# table
user = Table("user", metadata,
        Column("id", Integer, nullable=False, primary_key=True, autoincrement=True),
        Column("username", String(20), nullable=False),
        Column("age", Integer, nullable=False),
        Column("sex", SmallInteger, default=1),
        Column("create_time", DateTime, default=datetime.now)
    )

# model
class User(object):
    def __init__(self, username=None, age=None, sex=None):
        if username:
            self.username = username
        if age:
            self.age =age
        if sex:
            self.sex =sex

# table与model映射
mapper(User, user)


if __name__ == "__main__":
    # metadata.create_all(bind=engine)  #建表
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        user = User("rose", 20, 0)
        session.add(user)
        session.commit()
    except Exception as e:
        print(e)
        session.rollback()
    session.close()
