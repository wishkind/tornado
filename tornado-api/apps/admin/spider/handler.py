import json
import base64
import time

import requests
from blog.handler import RedisHandler

from apps.utils.mt_font_decode import modify_html
from apps.utils.utils import url_encode, url_decode, dict_to_str


class GetMTMInfoToken(RedisHandler):
    async def post(self, *args, **kwargs):
        data = self.request.body.decode()
        data = json.loads(base64.b64decode(data).decode())
        res = requests.post('http://api.qinjiahu.cn/m_info_token', json=data)
        self.finish(json.loads(res.text))


class GetFontDecode(RedisHandler):
    async def post(self, *args, **kwargs):
        data = self.request.body.decode()
        data = json.loads(base64.b64decode(data).decode())
        if data['font']:
            self.finish(modify_html(''.join(data['font'].split(';'))))
        else:
            self.finish('')


class GetWXListToken(RedisHandler):
    async def post(self, *args, **kwargs):
        data = self.request.body.decode()
        data = json.loads(base64.b64decode(data).decode())['post_data']

        sign_data = {
            'category_type': '0', 'lch': '1001', 'load_type': '1', 'navigate_type': '0', 'page_index': '4',
            'page_size': '20', 'partner': '4', 'platform': '13', 'req_time': '1554888784380', 'riskLevel': '1',
            'slider_select_data': '""', 'sort_type': '0', 'uuid': 'f70d0278-4b10-4b5b-80c8-6d5bde324778',
            'waimai_sign': '/', 'wm_actual_latitude': '30185340', 'wm_actual_longitude': '120264570',
            'wm_appversion': '3.8.5', 'wm_ctype': 'wxapp', 'wm_dplatform': 'devtools', 'wm_dtype': 'iPhone 6 Plus',
            'wm_dversion': '6.6.3', 'wm_latitude': '30185340', 'wm_longitude': '120264570',
            'wm_uuid': 'f70d0278-4b10-4b5b-80c8-6d5bde324778', 'wm_visitid': '8c47b325-f4d1-4e98-9434-1a2b62f2f04d'
        }

        for key, value in sign_data.items():
            sign_data[key] = data.get(key, value)

        sign = url_encode(json.dumps(dict_to_str(sign_data)), False).decode()

        token_data = {
            "rId": 100016,
            "ts": str(int(time.time()) * 1000),
            "cts": str(int(time.time()) * 1000 + 1258745),
            "brVD": [414, 624],
            "brR": [[1242, 1872], [1242, 1872], 24, 24],
            "bI": ["pages/index/index", ""],
            "mT": [],
            "kT": [],
            "aT": [],
            "tT": [],
            "sign": sign
        }
        token = url_encode(json.dumps(token_data)).decode()

        self.finish(token)


class GetWXInfoToken(RedisHandler):
    async def post(self, *args, **kwargs):
        data = self.request.body.decode()
        data = json.loads(base64.b64decode(data).decode())['post_data']

        sign_data = {
            'lch': '1001', 'open_id': '', 'partner': '4', 'platform': '13',
            'rank_list_id': '13414c4eee1bf3a7e-1986-4d80-879f', 'ref_list_id': '13414c4ad2a23fb15f017f-1986-4d80',
            'req_time': '1554996979437', 'riskLevel': '1', 'userToken': '', 'user_id': '', 'userid': '',
            'utm_source': '',
            'uuid': 'e901abc5-1986-4d80-879f-ec13011a5fba', 'waimai_sign': '/', 'wm_actual_latitude': '30257270',
            'wm_actual_longitude': '120205230', 'wm_appversion': '3.8.5', 'wm_channel': '', 'wm_ctype': 'wxapp',
            'wm_did': '', 'wm_dplatform': 'devtools', 'wm_dtype': 'iPhone 7 Plus', 'wm_dversion': '6.6.3',
            'wm_latitude': '30257680', 'wm_logintoken': '', 'wm_longitude': '120204748', 'wm_mac': '',
            'wm_uuid': 'e901abc5-1986-4d80-879f-ec13011a5fba', 'wm_visitid': '2d2fbe34-a619-49f0-abab-8ca316d8c165',
            'wmpoiid': '904332313437803'
        }

        for key, value in sign_data.items():
            sign_data[key] = data.get(key, value)

        sign = url_encode(json.dumps(dict_to_str(sign_data)), False).decode()

        token_data = {
            "rId": 100016,
            "ts": str(int(time.time()) * 1000),
            "cts": str(int(time.time()) * 1000 + 18345),
            "brVD": [414, 624],
            "brR": [[1242, 1872], [1242, 1872], 24, 24],
            "bI": ["pages/restaurant/restaurant", "pages/index/index"],
            "mT": [],
            "kT": [],
            "aT": [],
            "tT": [],
            "sign": sign
        }
        token = url_encode(json.dumps(token_data)).decode()

        self.finish(token)

