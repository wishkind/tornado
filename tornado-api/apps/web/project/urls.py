from tornado.web import url

from blog.settings import settings

from apps.web.project.handler import GetProjectHandler


get_project = '{}/project/get'.format(settings['BASE_WEB_URL'])


url_pattern = (
    url(get_project, GetProjectHandler),
)
