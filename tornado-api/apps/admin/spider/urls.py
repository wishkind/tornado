from tornado.web import url

from apps.admin.spider.handler import *

from blog.settings import settings


m_info_token = '{}/spider/m_info_token?'.format(settings['BASE_ADMIN_URL'])
m_info_font_decode = '{}/spider/font_decode?'.format(settings['BASE_ADMIN_URL'])
wx_list_token = '{}/spider/wx_list_token?'.format(settings['BASE_ADMIN_URL'])
wx_info_token = '{}/spider/wx_info_token?'.format(settings['BASE_ADMIN_URL'])


url_pattern = (
    url(m_info_token, GetMTMInfoToken),
    url(m_info_font_decode, GetFontDecode),
    url(wx_list_token, GetWXListToken),
    url(wx_info_token, GetWXInfoToken),
)
