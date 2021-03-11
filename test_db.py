import asyncio
import peewee
import peewee_async


database = peewee_async.PostgresqlDatabase(
   database="postgres",
   user="postgres",
   host="127.0.0.1",
   port="5432",
   password="dragon"
  )


class TestModel(peewee.Model):
    text  = peewee.CharField()
    class Meta:
        database = database


async def test():
    obj = await peewee_async.create_object(TestModel, text="good")
    obi_id = obj.id

    try:
        async with database.atomic_async():
            obj.text = "bar"
            await peewee_async.update_object(obj)
    except:
        res = await peewee_async.get_object(TestModel)
        print(res.text)

loop = asyncio.get_event_loop()
loop.run_until_complete(test())


