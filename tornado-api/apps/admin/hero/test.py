import json

from peewee_async import Manager
from playhouse.shortcuts import model_to_dict

from apps.models.article_models import ArticleModel
from apps.models.hero_models import HeroModels

from blog.settings import database


async def test():

    objects = Manager(database)
    database.set_allow_sync(False)

    hero = HeroModels.extends()

    hero = await objects.execute(
        hero.filter(HeroModels.state != 100)
    )

    for a in hero:
        print(model_to_dict(a))


if __name__ == '__main__':
    import asyncio

    loop = asyncio.get_event_loop()
    loop.run_until_complete(test())
