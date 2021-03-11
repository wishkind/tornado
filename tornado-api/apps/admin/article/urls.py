from tornado.web import url

from blog.settings import settings
from apps.admin.article.handler import *


article_url = '{}/article?'.format(settings['BASE_ADMIN_URL'])
article_all = '{}/article/all?'.format(settings['BASE_ADMIN_URL'])
operation_article_url = '{}/article/(.*?)?'.format(settings['BASE_ADMIN_URL'])

# 获取文章草稿箱列表
get_sketch = '{}/sketch/get?'.format(settings['BASE_ADMIN_URL'])
# 删除草稿箱
del_sketch = '{}/sketch/del/(.*?)?'.format(settings['BASE_ADMIN_URL'])
# 发布
push_sketch = '{}/sketch/push/(.*?)?'.format(settings['BASE_ADMIN_URL'])
# 批量操作
all_sketch = '{}/sketch/all?'.format(settings['BASE_ADMIN_URL'])

# 获取已删除文章列表
get_articleR = '{}/articleR/get?'.format(settings['BASE_ADMIN_URL'])
# 彻底删除
del_articleR = '{}/articleR/del/(.*?)?'.format(settings['BASE_ADMIN_URL'])
# 还原已删除文章
edit_articleR = '{}/articleR/edit/(.*?)?'.format(settings['BASE_ADMIN_URL'])
# 批量操作已删除文章
all_articleR = '{}/articleR/all?'.format(settings['BASE_ADMIN_URL'])


url_pattern = (
    url(article_url, ArticleHandler),
    url(article_all, EditAllArticleHandler),
    url(operation_article_url, OperationArticleHandler),
    url(get_sketch, GetSketchHandler),
    url(del_sketch, DelSketchHandler),
    url(push_sketch, PushSketchHandler),
    url(all_sketch, AllSketchHandler),
    url(get_articleR, GetArticleRHandler),
    url(del_articleR, DelArticleRHandler),
    url(edit_articleR, EditArticleRHandler),
    url(all_articleR, AllArticleRHandler)
)
