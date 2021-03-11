from tornado.web import url

from apps.web.tags.handler import TagHandler
from blog.settings import settings


tag = settings['BASE_WEB_URL'] + '/tag/get?'


url_pattern = (
    url(tag, TagHandler),
)
