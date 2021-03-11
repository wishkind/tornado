from tornado.web import url

from apps.admin.test.handler import TextHandler, MtTuanTokenHandler

from blog.settings import settings


test_url = '{}/test/(.*?)?'.format(settings['BASE_ADMIN_URL'])
mt_token_url = '{}/mt_token?'.format(settings['BASE_ADMIN_URL'])


url_pattern = (
    url(test_url, TextHandler),
    url(mt_token_url, MtTuanTokenHandler),
)
