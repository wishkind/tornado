from tornado.web import url

from apps.admin.project.handler import *

from blog.settings import settings


get_project = '{}/project/get?'.format(settings['BASE_ADMIN_URL'])
put_project = '{}/project/put?'.format(settings['BASE_ADMIN_URL'])
del_project = '{}/project/del/(.*?)?'.format(settings['BASE_ADMIN_URL'])
edit_project = '{}/project/edit/(.*?)?'.format(settings['BASE_ADMIN_URL'])
all_project = '{}/project/all?'.format(settings['BASE_ADMIN_URL'])
filter_project = '{}/project/filter?'.format(settings['BASE_ADMIN_URL'])

get_id_project = '{}/project/get/(.*?)?'.format(settings['BASE_ADMIN_URL'])


url_pattern = (
    url(get_project, GetProjectHandler),
    url(put_project, PutProjectHandler),
    url(del_project, DelProjectHandler),
    url(edit_project, EditProjectHandler),
    url(all_project, AllProjectHandler),
    url(get_id_project, GetIdProjectHandler),
    url(filter_project, FilterProjectHandler),
)
