from tornado.web import url

from blog.settings import settings

from apps.web.note.handler import GetNoteHandler


get_note = '{}/note/get'.format(settings['BASE_WEB_URL'])


url_pattern = (
    url(get_note, GetNoteHandler),
)
