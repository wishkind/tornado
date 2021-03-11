import peewee 
import peewee_async
import asyncio
import psycopg2
import aiopg
db = peewee_async.MySQLDatabase("deng",host="127.0.0.1",\
       port=3306,user="root",password="dragon")

class Goods(peewee.Model):
    name = peewee.CharField(max_length=100,verbose_name="商品名字",index=True)
    click_num = peewee.IntegerField(default=0,verbose_name="点击数")
    goods_num = peewee.IntegerField(default=0,verbose_name="库存")
    price = peewee.FloatField(default=0.0,verbose_name="商品价格")
    brief = peewee.TextField(verbose_name="商品简介")
    
    
    class Meta:
        database = db

def init_table():
    db.create_tables([Goods])
    db.close()
if __name__ == "__main__":
    init_table()
