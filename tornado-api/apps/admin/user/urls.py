from tornado.web import url
from apps.admin.user.handle import LoginHandle, UserHandler
from blog.settings import settings


login_url = '{}/user/login/?'.format(settings['BASE_ADMIN_URL'])
user_url = '{}/user/?'.format(settings['BASE_ADMIN_URL'])

url_pattern = (
    url(login_url, LoginHandle),
    url(user_url, UserHandler),
)
