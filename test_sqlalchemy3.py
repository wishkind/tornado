# -*- coding: utf-8 -*-
import pymysql.connections
import pymysql.converters
import pymysql.cursors
pymysql.install_as_MySQLdb()
import MySQLdb
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from datetime import datetime

engine = create_engine("mysql+mysqldb://root:123456@127.0.0.1/todo?charset=utf8")

Base = automap_base()
Base.prepare(engine, reflect=True)

# 反射得到orm
Human = Base.classes.human

# 通信
session = Session(bind=engine)


# 插入数据
def insert():
    h = Human(name="vcr", age=67, sex=1, create_time=datetime.now())
    session.add(h)
    #session.add_all([x,y])
    session.commit()

# 修改数据
def update():
    h_obj = session.query(Human).filter_by(name="vcr").first()
    h_obj.name = "vccrr"
    session.add(h_obj)
    session.commit()

# 删除数据
def delete():
    h_obj = session.query(Human).filter_by(name="vccrr").first()
    session.delete(h_obj)
    session.commit()

# 查询数据
def select():
    res = session.query(Human).filter(Human.id > 7)
    print([i for i in res])


if __name__ == "__main__":
    select()
