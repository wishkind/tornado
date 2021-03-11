import peewee
import asyncio
import peewee_async


database = peewee_async.PostgresqlDatabase(
                database='postgres',
                user='postgres',
                host='127.0.0.1',
                port='5432',
                password='dragon'
    )
loop1 = asyncio.get_event_loop()


class TestModel(peewee.Model):
    text  = peewee.CharField()
    class Meta:
        database = database



TestModel.create_table(True)
TestModel.create(text='good night')
database.close()
