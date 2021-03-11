from tornado.web import url

from apps.admin.note.handler import *

from blog.settings import settings


get_note = '{}/note/get?'.format(settings['BASE_ADMIN_URL'])
add_note = '{}/note/put?'.format(settings['BASE_ADMIN_URL'])
del_note = '{}/note/del/(.*?)?'.format(settings['BASE_ADMIN_URL'])
edit_note = '{}/note/edit/(.*?)?'.format(settings['BASE_ADMIN_URL'])

get_id_note = '{}/note/get/(.*?)?'.format(settings['BASE_ADMIN_URL'])

all_note = '{}/note/all?'.format(settings['BASE_ADMIN_URL'])
filter_note = '{}/note/filter?'.format(settings['BASE_ADMIN_URL'])


url_pattern = (
    url(get_note, GetNoteHandler),
    url(add_note, AddNoteHandler),
    url(del_note, DelNoteHandler),
    url(edit_note, EditNoteHandler),
    url(get_id_note, GetIdNoteHandler),
    url(all_note, AllNoteHandler),
    url(filter_note, FilterNoteHandler)
)
