from tornado.web import url


from apps.web.comment.handler import CommentHandler, PutCommentHandler, LikeCommentHandler
from blog.settings import settings


comment_url = '{}/comment/get?'.format(settings['BASE_WEB_URL'])
put_comment = '{}/comment/add?'.format(settings['BASE_WEB_URL'])
like_comment = '{}/comment/like/(.*?)?'.format(settings['BASE_WEB_URL'])


url_pattern = (
    url(comment_url, CommentHandler),
    url(put_comment, PutCommentHandler),
    url(like_comment, LikeCommentHandler)
)
