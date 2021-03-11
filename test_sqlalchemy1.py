# -*- coding: utf-8 -*-

from datetime import datetime

import pymysql.connections
import pymysql.converters
import pymysql.cursors
pymysql.install_as_MySQLdb()
import MySQLdb

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (create_engine, Column, Integer, String, SmallInteger, DateTime)
from sqlalchemy.orm import Session

engine = create_engine("mysql+mysqldb://root:dragon@127.0.0.1/deng?charset=utf8")
Base = declarative_base()


class Human(Base):
    __tablename__ = "human"
    id = Column("id", Integer, autoincrement=True, primary_key=True)
    name = Column("name", String(20), nullable=False, unique=True)
    age = Column("age", Integer, nullable=False)
    sex = Column("sex", SmallInteger, default=1)
    create_time = Column("create_time", DateTime, default=datetime.now)

    def __repr__(self):
        return "name {}".format(self.name)


if __name__ == "__main__":
    # Base.metadata.create_all(bind=engine) # 建表
    session = Session(bind=engine)
    # h = Human(name="king001", age=30, sex=1)
    # session.add(h)
	
	# Human.__table__ ------------------------------>orm转经典类型(table类型)
	
    try:
        res = []
        for i in range(2,11):
            h = Human(name="king00{}".format(str(i)), age=i, sex=1)
            res.append(h)

        session.add_all(res)
        session.commit()
    except Exception as e:
        print(e)
        session.rollback()
    session.close()
