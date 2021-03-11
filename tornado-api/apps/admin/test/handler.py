import base64
import time
import zlib
import json
from urllib.parse import urlencode
from blog.handler import RedisHandler


class TextHandler(RedisHandler):
    async def get(self, request_code, *args, **kwargs):
        self.finish('hello test!!!')


class MtTuanTokenHandler(RedisHandler):
    async def post(self, *args, **kwargs):
        data = json.loads(self.request.body.decode())
        sign = self.url_encode(urlencode(data)).decode()
        data = {
            "rId": 0,
            "ts": int(time.time()) * 1000,
            "cts": int(time.time()) * 1000 + 2626269,
            "brVD": [
                360,
                554
            ],
            "brR": [
                [
                    1080,
                    1662
                ],
                [
                    1080,
                    1662
                ],
                24,
                24
            ],
            "bI": [
                "pages/restaurant/restaurant",
                "pages/index/index"
            ],
            "mT": [

            ],
            "kT": [

            ],
            "aT": [

            ],
            "tT": [

            ],
            "sign": sign
        }
        token = self.url_encode(json.dumps(data)).decode()
        self.finish(token)

    def url_encode(self, data):
        """token解码"""
        if isinstance(data, str):
            data = data.replace(" ", "").encode()
            base_data = zlib.compress(data)
            data = base64.b64encode(base_data)
            return data
        else:
            data = str(data)
            return self.url_encode(data)

