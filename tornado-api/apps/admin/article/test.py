import json

from peewee_async import Manager
from apps.models.article_models import ArticleModel

from blog.settings import database


async def test():

    objects = Manager(database)
    database.set_allow_sync(False)

    # article = ArticleModel.select().filter(ArticleModel.tag=='react')
    # tags = await objects.execute(ArticleModel.select().where(ArticleModel.tag=='react'))

    # tag = await objects.get(TagModel, name='vue')
    tag = {'content': '在网页中浏览器资源开销最大便是DOMdddddddd节点了，DOM很慢并且非常庞大', 'title': '浅析虚拟dom原理并实现', 'desc': '讲讲虚拟dom原理和简单的实现', 'edit_content': '在网页中浏览器资源开销最大便是DOM节点了，DOM很慢并且非常庞大', 'keyword': 'vue', 'tag': ['1', '3']}

    await objects.create(ArticleModel, content=tag['content'], title=tag['title'],
                         desc=tag['desc'], tag='cue', keyword=tag['keyword'])

    # print(model_to_dict(tag))

    # for i in tags:
    #     print(i.id)


if __name__ == '__main__':
    # import asyncio
    #
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(test())

    a = b'{"content":"\xe5\x9c\xa8\xe7\xbd\x91\xe9\xa1\xb5\xe4\xb8\xad\xe6\xb5\x8f\xe8\xa7\x88\xe5\x99\xa8\xe8\xb5\x84\xe6\xba\x90\xe5\xbc\x80\xe9\x94\x80\xe6\x9c\x80\xe5\xa4\xa7\xe4\xbe\xbf\xe6\x98\xafDOM\xe8\x8a\x82\xe7\x82\xb9\xe4\xba\x86\xef\xbc\x8cDOM\xe5\xbe\x88\xe6\x85\xa2\xe5\xb9\xb6\xe4\xb8\x94\xe9\x9d\x9e\xe5\xb8\xb8\xe5\xba\x9e\xe5\xa4\xa7","title":"\xe6\xb5\x85\xe6\x9e\x90\xe8\x99\x9a\xe6\x8b\x9fdom\xe5\x8e\x9f\xe7\x90\x86\xe5\xb9\xb6\xe5\xae\x9e\xe7\x8e\xb0","desc":"\xe8\xae\xb2\xe8\xae\xb2\xe8\x99\x9a\xe6\x8b\x9fdom\xe5\x8e\x9f\xe7\x90\x86\xe5\x92\x8c\xe7\xae\x80\xe5\x8d\x95\xe7\x9a\x84\xe5\xae\x9e\xe7\x8e\xb0","edit_content":"\xe5\x9c\xa8\xe7\xbd\x91\xe9\xa1\xb5\xe4\xb8\xad\xe6\xb5\x8f\xe8\xa7\x88\xe5\x99\xa8\xe8\xb5\x84\xe6\xba\x90\xe5\xbc\x80\xe9\x94\x80\xe6\x9c\x80\xe5\xa4\xa7\xe4\xbe\xbf\xe6\x98\xafDOM\xe8\x8a\x82\xe7\x82\xb9\xe4\xba\x86\xef\xbc\x8cDOM\xe5\xbe\x88\xe6\x85\xa2\xe5\xb9\xb6\xe4\xb8\x94\xe9\x9d\x9e\xe5\xb8\xb8\xe5\xba\x9e\xe5\xa4\xa7","keyword":"vue","tag":["ed72e300f45f11e881f6005056c00007","c61dd30824164992b32da38c9b2de698","ed72e300f45f11e881f6005056c00006"]}'

    a = json.loads(a.decode('utf-8'))


# res = requests.get('http://127.0.0.1:9999/api/v1/tag/add')
# print(res)
