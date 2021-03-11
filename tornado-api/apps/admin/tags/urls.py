from tornado.web import url

from apps.admin.tags.handler import TagHandler
from blog.settings import settings


tag = settings['BASE_ADMIN_URL'] + '/tag/?'


url_pattern = (
    url(tag, TagHandler),
)
