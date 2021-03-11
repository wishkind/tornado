from tornado.web import url

from blog.settings import settings

from apps.web.article.handler import ArticleHandler, ArticleIDHandler, LikeArticleHandler, getAllArticleHandler


get_article = '{}/article/get?'.format(settings['BASE_WEB_URL'])
get_all_article = '{}/article/getAll?'.format(settings['BASE_WEB_URL'])
get_id_article = '{}/article/get/(.*?)?'.format(settings['BASE_WEB_URL'])

like_article = '{}/article/like/(.*?)?'.format(settings['BASE_WEB_URL'])


url_pattern = (
    url(get_article, ArticleHandler),
    url(get_id_article, ArticleIDHandler),
    url(like_article, LikeArticleHandler),
    url(get_all_article, getAllArticleHandler)
)
