from tornado.web import url

from blog.settings import settings

from apps.admin.reply.handler import *


get_reply = '{}/reply/get?'.format(settings['BASE_ADMIN_URL'])
edit_reply = '{}/reply/edit/(.*?)?'.format(settings['BASE_ADMIN_URL'])
del_reply = '{}/reply/del/(.*?)?'.format(settings['BASE_ADMIN_URL'])

edit_all_reply = '{}/reply/all?'.format(settings['BASE_ADMIN_URL'])
filter_reply = '{}/reply/filter/(.*?)?'.format(settings['BASE_ADMIN_URL'])


url_pattern = (
    url(get_reply, GetReplyHandler),
    url(del_reply, DelReplyHandler),
    url(edit_reply, EditReplyHandler),
    url(edit_all_reply, EditAllReplyHandler),
    url(filter_reply, FilterReplyHandler)
)
