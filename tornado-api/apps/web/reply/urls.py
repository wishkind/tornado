from tornado.web import url

from blog.settings import settings

from apps.web.reply.handler import PutReplyHandler, GetReplyHandler


put_reply = '{}/reply/add?'.format(settings['BASE_WEB_URL'])
get_reply = '{}/reply/get/(.*?)?'.format(settings['BASE_WEB_URL'])


url_pattern = (
    url(put_reply, PutReplyHandler),
    url(get_reply, GetReplyHandler)
)

