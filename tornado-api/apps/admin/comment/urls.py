from tornado.web import url

from blog.settings import settings

from apps.admin.comment.handler import *


get_comment = '{}/comment/get?'.format(settings['BASE_ADMIN_URL'])
del_comment = '{}/comment/delete/(.*?)?'.format(settings['BASE_ADMIN_URL'])
edit_comment = '{}/comment/edit/(.*?)?'.format(settings['BASE_ADMIN_URL'])
edit_all_comment = '{}/comment/all?'.format(settings['BASE_ADMIN_URL'])
filter_comment = '{}/comment/filter/(.*?)?'.format(settings['BASE_ADMIN_URL'])


url_pattern = (
    url(get_comment, GetCommentHandler),
    url(edit_comment, EditCommentHandler),
    url(del_comment, DelCommentHandler),
    url(edit_all_comment, EditAllCommentHandler),
    url(filter_comment, FilterCommentHandler)
)
