from tornado.web import url

from apps.admin.hero.handler import *

from blog.settings import settings


get_hero = '{}/hero/get?'.format(settings['BASE_ADMIN_URL'])
edit_hero = '{}/hero/edit/(.*?)?'.format(settings['BASE_ADMIN_URL'])
edit_all_hero = '{}/hero/all?'.format(settings['BASE_ADMIN_URL'])
filter_hero = '{}/hero/filter?'.format(settings['BASE_ADMIN_URL'])
del_hero = '{}/hero/delete/(.*?)?'.format(settings['BASE_ADMIN_URL'])

get_heroR = '{}/heroR/get?'.format(settings['BASE_ADMIN_URL'])
edit_heroR = '{}/heroR/edit/(.*?)?'.format(settings['BASE_ADMIN_URL'])
edit_all_heroR = '{}/heroR/all?'.format(settings['BASE_ADMIN_URL'])
del_heroR = '{}/heroR/delete/(.*?)?'.format(settings['BASE_ADMIN_URL'])


url_pattern = (
    url(get_heroR, GetHeroRHandler),
    url(edit_heroR, EditHeroRHandler),
    url(edit_all_heroR, EditAllHeroRHandler),
    url(del_heroR, DelHeroRHandler),

    url(get_hero, GetHeroHandler),
    url(edit_hero, EditHeroHandler),
    url(edit_all_hero, EditAllHandler),
    url(filter_hero, FilterHandler),
    url(del_hero, DelHeroHandler)
)
