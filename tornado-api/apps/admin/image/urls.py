from tornado.web import url

from blog.settings import settings
from apps.admin.image.handler import ImageHandler


images_url = settings['BASE_ADMIN_URL'] + '/images'


url_pattern = (
    url(images_url, ImageHandler),
)
