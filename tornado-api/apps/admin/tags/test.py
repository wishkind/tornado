import requests
from peewee_async import Manager
from apps.models.article_models import ArticleModel

from blog.settings import database


async def test():

    objects = Manager(database)
    database.set_allow_sync(False)

    # article = ArticleModel.select().filter(ArticleModel.tag=='react')
    # tags = await objects.execute(ArticleModel.select().where(ArticleModel.tag=='react'))

    tag = await objects.count(ArticleModel.select(ArticleModel.tag))

    print(tag)


def test1():
    r = requests.delete('http://127.0.0.1:9999/api/v1/user', json={
        'username': 'react1',
        'uuid': 'd147fbf97b0cef765d5de40329dbd08c'
    })

    print(r.text)


if __name__ == '__main__':
    test1()
    # import asyncio
    #
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(test())
