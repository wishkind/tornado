import time
import asyncio
import tornado.gen
import tornado.web
import tornado.ioloop
import tornado.httpserver
from tornado.options import define, options
from tornado.httpclient import HTTPClient, AsyncHTTPClient
from requests import get

settings = {'debug': True}
url = "http://127.0.0.1:8888/"


def synchronous_fetch(url):
    print("sync")
    try:
        http_client = HTTPClient()
        time.sleep(5)
        response = http_client.fetch(url)
        print(response.body)
    except Exception as e:
        print("Error:" + str(e))
        return str(e)
    http_client.close()
    return response.body

def synchronous_get(url):
    response = get(url)
    time.sleep(5)
    print("sync")
    return response.text

async def sleep():
    print("start")
    await asyncio.sleep(5)
    print("end")

async def async_fetch(url):
    http_client = AsyncHTTPClient()
    response = await http_client.fetch(url)
    print("async")
    return response.body


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("hello: %s" % self.request.request_time())
        self.finish()
        print("not finish")
        return 

class synchronous_fetcher(tornado.web.RequestHandler):
    def get(self):
        self.write("%s, %s" % (synchronous_fetch(url), self.request.request_time()))

class synchronous_geter(tornado.web.RequestHandler):
    def get(self):
        self.write("%s, %s" % (synchronous_get(url), self.request.request_time()))

class asynchronous_fetcher_1(tornado.web.RequestHandler):
    async def get(self):
        body = await async_fetch(url)
        for i in range(3):
            print("skip %s" % i)
            await tornado.gen.sleep(5)
        time.sleep(5)
        print("end request")
        self.write("%s, %s" % (body, self.request.request_time()))


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/1", asynchronous_fetcher_1),
        (r"/2", synchronous_fetcher),
        (r"/3", synchronous_geter),
      ], **settings)

if __name__ == '__main__':
    print("begin")
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()

