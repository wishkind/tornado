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
objects = peewee_async.Manager(database)

database.set_allow_sync(False)

async def handler():
    await objects.create(TestModel, text="not bad")
    all_objects = await objects.execute(TestModel.select())
    for obj in all_objects:
        print(obj.text)
loop = asyncio.get_event_loop()
loop.run_until_complete(handler())
loop.close()

with objects.allow_sync():
    TestModel.drop_table(True)

@asyncio.coroutine
def my_handler():
    obj1 = TestModel.create(text="gfkjgfhk")
    obj2 = yield from peewee_async.create_object(TextModel, text="hello")
    all_objects = yield from peewee_async.execute(TestModel.select())
    for obj in all_objects:
        print(obj.text)

    obj1.delete_instance()
    yield from peewee_aync.delete_object(obj2)
"""
loop1.run_until_complete(database.connect_async(loop=loop)

loop1.run_until_complete(my_handler())


async def test():
    obj = await create_object(TestModel, text="good")
    obi_id = obj.id

    try:
        async with database.atomic_async(): 
            obj.text = "bar"
            await update_object(obj)
            raise Exception('Fake error')
    except:
        res = await get_object(TestModel, test="hffh")
    print(res.text)

loop1.run_until_complete(test())"""
