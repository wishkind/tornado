import os

from tornado.web import url

from blog.settings import settings
from blog.handler import MyFileHandler

from apps.admin.user.urls import url_pattern as user_urls
from apps.admin.tags.urls import url_pattern as tag_urls
from apps.admin.article.urls import url_pattern as article_urls
from apps.admin.image.urls import url_pattern as upload_image_urls
from apps.admin.comment.urls import url_pattern as comment_urls
from apps.admin.reply.urls import url_pattern as reply_urls
from apps.admin.hero.urls import url_pattern as hero_urls
from apps.admin.test.urls import url_pattern as text_urls
from apps.admin.note.urls import url_pattern as note_urls
from apps.admin.project.urls import url_pattern as project_urls
from apps.admin.spider.urls import url_pattern as spider_urls


image_url = settings['BASE_ADMIN_URL'] + '/media/images/(.*?)?'

url_pattern = (
    url(image_url, MyFileHandler, {'path': os.path.join(settings["MEDIA_ROOT"], 'images')}),
)

url_pattern += user_urls
url_pattern += tag_urls
url_pattern += article_urls
url_pattern += comment_urls
url_pattern += upload_image_urls
url_pattern += reply_urls
url_pattern += hero_urls
url_pattern += text_urls
url_pattern += note_urls
url_pattern += project_urls
url_pattern += spider_urls

