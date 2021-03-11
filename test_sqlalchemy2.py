# -*- coding: utf-8 -*-
import pymysql.connections
import pymysql.converters
import pymysql.cursors
pymysql.install_as_MySQLdb()
import MySQLdb

from datetime import datetime
from sqlalchemy import Table, create_engine, MetaData, select, func

engine = create_engine("mysql+mysqldb://root:123456@127.0.0.1/todo?charset=utf8")
metadata = MetaData()

# 开启一个连接
conn = engine.connect()

# 反射表
human = Table("human", metadata, autoload=True, autoload_with=engine)

#反射库
metadata.reflect(bind=engine)
human = metadata.tables.get('human')

# 批量插入
def insert():
    ins = human.insert()
    conn.execute(ins, {"name":"ppp","age":20,"sex":1})
    conn.execute(ins, [{"name":"ppp","age":20,"sex":1},{"name":"mmm","age":30,"sex":0}])
    conn.close()

# 插入2
def insert2():
    ins = human.insert().values(name="bbb", age=40, sex=0, create_time=datetime.now())
    conn.execute(ins)
    conn.close()

# 修改
def update():
    up = human.update().values(name="vvv").where(human.c.name=="bbb")
    conn.execute(up)
    conn.close()

# 删除
def delete():
    de = human.delete().where(human.c.name=="vvv")
    conn.execute(de)
    conn.close()

# 查询
def _select():
    s = select([human.c.name, human.c.age]).where(human.c.age>20).limit(2).offset(0)
    res = conn.execute(s)
    print(res.fetchall())

# 查询2
def _select2():
    s = select([human.c.sex, func.count(human.c.id), func.sum(human.c.age)]).group_by(human.c.sex)
    res = conn.execute(s)
    print(res.fetchall())

#product---->project---->requirement
# 查询3(连接查询)
def select3():
    i = requirement.join(project, project.c.id==requirement.c.prj_id).join(product, product.c.id==project.c.prod_id)
    s = select([project.c.prj_name.label("prj_name"), product.c.prod_name.label("prod_name"), requirement.c.req_name.label("req_name")]).select_from(i)
    res = self.conn.execute(s).fetchall()
####################################################################
# 注意：多次连表查询，xxx_table.join(xx,xx==xx).join(xx,xx==xx)以此类推
####################################################################
"""
SELECT project.prj_name AS prj_name, product.prod_name AS prod_name, requirement.req_name AS req_name 
FROM requirement JOIN project ON project.id = requirement.prj_id JOIN product ON product.id = project.prod_id
"""

if __name__ == "__main__":
    _select2()

