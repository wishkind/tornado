import json

from peewee_async import Manager
from playhouse.shortcuts import model_to_dict
from apps.utils.utils import json_serial
from apps.models.article_models import ArticleModel
from apps.models.tag_models import TagModel
from apps.models.hero_models import HeroModels

from blog.settings import database


async def test():

    objects = Manager(database)
    database.set_allow_sync(False)

    article = ArticleModel.select().order_by(ArticleModel.id.desc())
    articles = await objects.execute(article)

    article_data = {}
    article_list = []
    month_set = set()

    for article in articles:
        article_dict = model_to_dict(article)
        print(article_dict)
        year = str(article_dict['update_time'].year)
        month = str(article_dict['update_time'].month)
        tag_list = []
        for tag in str(article_dict['tag']).split('|'):
            if tag:
                tag = await objects.get(TagModel, name=tag)
                tag_list.append(model_to_dict(tag))

        article_dict['tag'] = tag_list

        if year not in article_data.values():
            article_year = article_data.get(year, None)
            if article_year:
                for year in article_year:
                    if year.get(month, None):
                        year[month].append(article_dict)
                        month_set.add(month)

                    else:
                        if month not in month_set:
                            year[month] = [article_dict]
                            month_set.add(month)

            else:
                _month = {}
                _month[month] = [article_dict]
                article_data[year] = [_month]

    for article_key, article_value in article_data.items():
        month_list = []
        for month_data in article_value:
            for month_key, month_value in month_data.items():
                month_list.append({
                    'articleList': month_value,
                    'month': month_key
                })
        article_list.append({
            'year': article_key,
            'monthList': month_list
        })

    print(json.dumps(article_list, default=json_serial))


async def test1():
    objects = Manager(database)
    database.set_allow_sync(False)

    article = ArticleModel.select().order_by(ArticleModel.update_time.desc())
    articles = await objects.execute(article)
    for ar in articles:
        print(model_to_dict(ar))


if __name__ == '__main__':
    import asyncio

    loop = asyncio.get_event_loop()
    loop.run_until_complete(test1())
