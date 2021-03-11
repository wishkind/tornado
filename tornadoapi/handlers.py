
import asyncio
from datetime import datetime
import json
import logging
import requests

import tornado.httpclient
import tornado.web


logger = logging.getLogger(__name__)


class HomeHandler(tornado.web.RequestHandler):

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    async def get(self):

        await asyncio.sleep(1)

        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")

        self.write({"message": current_time})


class RecommendationsHandler(tornado.web.RequestHandler):

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    async def post(self):

        await asyncio.sleep(1)
        url = "https://news-api.lateral.io/documents/similar-to-text"

        payload = json.dumps({"text": str(self.request.body, 'utf-8')})
        headers = {
            'subscription-key': "f53dd4aea5bfc8ecd850fcbe1b08921e",
            'content-type': "application/json",
            'Accept': "text/plain"
        }

        response = requests.request("POST", url, data=payload, headers=headers)
        self.write({"results": response.text})



