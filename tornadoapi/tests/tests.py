
import asyncio
import sys
sys.path.append('..')

from tornado.platform.asyncio import AsyncIOLoop
from tornado.testing import AsyncHTTPTestCase, gen_test

import app


class AsyncIOLoopTest(AsyncHTTPTestCase):
    def get_app(self):
        return app.get_app()


    def get_new_ioloop(self):
        io_loop = AsyncIOLoop()
        asyncio.set_event_loop(io_loop.asyncio_loop)
        return io_loop


    @gen_test
    async def test_homepage(self):
        response = await self.http_client.fetch(self.get_url('/'))

        self.assertEqual(response.code, 200, "homepage returned a different status code")

