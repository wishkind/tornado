from datetime import datetime
import peewee
import peewee_async
import asyncio
from blog.settings import database
from peewee import Model, DateTimeField


class BaseModel(Model):
    create_time = DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        database = database



database = peewee_async.PostgresqlDatabase(
                database='postgres',
                user='postgres',
                host='127.0.0.1',
                port='5432',
                password='dragon'
    )
loop1 = asyncio.get_event_loop()


class BaseModel(peewee.Model):
    text  = peewee.CharField()
    create_time = peewee.DateTimeField(default=datetime.now, verbose_name=''添加时间')
    class Meta:
        database = database



BaseModel.create_table(True)
BaseModel.create(text='good night')
database.close()
objects = peewee_async.Manager(database)

database.set_allow_sync(False)

async def handler():
    await objects.create(BaseModel, text="not bad")
    all_objects = await objects.execute(BaseModel.select())
    for obj in all_objects:
        print(obj.text)
loop = asyncio.get_event_loop()
loop.run_until_complete(handler())

