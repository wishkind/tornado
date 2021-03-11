import asyncio
import peewee
import peewee_async

database = peewee_async.PostgresqlDatabase(
    database ='postgres',
    user = 'postgres',
    host = '127.0.0.1',
    port = '5432',
    password = 'dragon'
)


<<<<<<< HEAD
=======
db = SqliteDatabase('people.db')

class Person(Model):

    name = CharField()
    birthday = DateField()
    is_relative = BooleanField() 
    class Meta:

        database = db #  这个模型使用 "people.db"数据库

class Pet(Model):

    owner = ForeignKeyField(Person, related_name='pets')
    name = CharField()
    animal_type = CharField()

    class Meta:
        database = db # 这个模型使用"people.db"数据库
db.connect()
from datetime import date
uncle_bob = Person(name='Bob', birthday=date(1960, 1, 15), is_relative=True)
uncle_bob.save() 

grandma = Person.create(name='Grandma', birthday=date(1935, 3, 1), is_relative=True)
herb = Person.create(name='Herb', birthday=date(1950, 5, 5), is_relative=False)

bob_kitty = Pet.create(owner=uncle_bob, name='Kitty', animal_type='cat')
herb_fido = Pet.create(owner=herb, name='Fido', animal_type='dog')
herb_mittens = Pet.create(owner=herb, name='Mittens', animal_type='cat')
herb_mittens_jr = Pet.create(owner=herb, name='Mittens Jr', animal_type='cat')
herb_mittens.delete_instance()


herb_fido.owner = uncle_bob
herb_fido.save()
bob_fido = herb_fido # 为了更清晰重命名我们的变量

grandma = Person.select().where(Person.name == ‘Grandma L.’).get()
for person in Person.select():
    print(person.name, person.is_relative)

query = Pet.select().where(Pet.animal_type == 'cat')
    for pet in query:
        print(pet.name, pet.owner.name)

query = (Pet.select(Pet, Person).join(Person).where(Pet.animal_type == 'cat'))
for pet in query:
    print(pet.name, pet.owner.name)

for pet in Pet.select().join(Person).where(Person.name == 'Bob'):
    print(pet.name)

for pet in Pet.select().where(Pet.owner == uncle_bob).order_by(Pet.name):
    print(pet.name)

for person in Person.select().order_by(Person.birthday.desc()):
    print(person.name, person.birthday)

for person in Person.select():
    print(person.name, person.pets.count(), 'pets')
        for pet in person.pets:
            print('    ', pet.name, pet.animal_type)

subquery = Pet.select(fn.COUNT(Pet.id)).where(Pet.owner == Person.id)
query = (Person.select(Person, Pet, 
             subquery.alias('pet_count'))
                  .join(Pet, JOIN.LEFT_OUTER)
                        .order_by(Person.name)) 

for person in query.aggregate_rows():  # 注意 `aggregate_rows()`的调用.
    print person.name, person.pet_count, 'pets')
    for pet in person.pets:
        print('    ', pet.name, pet.animal_type)


d1940 = date(1940, 1, 1)
d1960 = date(1960, 1, 1)
query = (Person
             .select()
                  .where((Person.birthday < d1940) | (Person.birthday > d1960)))

for person in query:
    print(person.name, person.birthday)


db.close()



>>>>>>> third commit
class TestModel(peewee.Model):
    text = peewee.CharField()

    class Meta:
        database = database


TestModel.create_table(True)
TestModel.create(text="yes I can do it sync")
database.close()

objects = peewee_async.Manager(database)

database.set_allow_sync(False)

async def handler():
    await objects.create(TestModel, text="Not bad. Watch this, I'm async!")
    all_objects = await objects.execute(TestModel.select())

    for obj in all_objects:
        print(obj.text)


loop = asyncio.get_event_loop()
loop.run_until_complete(handler())
loop.close()

with objects.allow_sync():
    TestModel.drop_table(True)
