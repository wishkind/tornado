# admin 后台管理的接口
from apps.admin import url_pattern as admin_urls

# 前端接口
from apps.web import url_pattern as web_urls

url_pattern = []

url_pattern += admin_urls
url_pattern += web_urls

import os

from tornado.web import url
from blog.settings import settings
from blog.handler import MyFileHandler

rom apps.admin.user.urls import url_pattern as user_urls
from apps.admin.tags.urls import url_pattern as tag_urls
from apps.admin.article.urls import url_pattern as article_urls
from apps.admin.image.urls import url_pattern as upload_image_urls


image_url = settings['BASE_ADMIN_URL'] + '/media/images/(.*?)?'


url_pattern = [(
    url(image_url, MyFileHandler, {'path': os.path.join(settings["MEDIA_ROOT"], 'images')})
 )]
#
url_pattern += user_urls
url_pattern += tag_urls
url_pattern += article_urls
url_pattern += upload_image_urls
