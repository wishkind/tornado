from apps.admin.user import UserModel

from peewee_async import Manager

from blog.settings import database


async def test():

    objects = Manager(database)
    database.set_allow_sync(False)

    # article = ArticleModel.select().filter(ArticleModel.tag=='react')
    # tags = await objects.execute(ArticleModel.select().where(ArticleModel.tag=='react'))

    tag = await objects.create(UserModel, username='admin123', password='admin123')

    print(tag)

    # for i in tags:
    #     print(i.id)


if __name__ == '__main__':
    import asyncio

    loop = asyncio.get_event_loop()
    loop.run_until_complete(test())
