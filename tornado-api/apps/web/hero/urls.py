from tornado.web import url

from apps.web.hero.handler import *
from blog.settings import settings


add_hero = '{}/hero/add?'.format(settings['BASE_WEB_URL'])
get_hero = '{}/hero/get?'.format(settings['BASE_WEB_URL'])


url_pattern = (
    url(add_hero, AddHeroHandler),
    url(get_hero, HeroHandler),
)
