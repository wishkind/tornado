import tornado.web
import time
import tornado.gen
import  tornado.concurrent
from concurrent.futures import ThreadPoolExecutor


class MainHandler(tornado.web.RequestHandler):
    executor=ThreadPoolExecutor(900)
    @tornado.concurrent.run_on_executor
    def db_query(self):
        print("start")
        time.sleep(10)
        print("close")
        self.write("ok")
    @tornado.gen.coroutine
    def get(self):
        self.write("fff                           good night")
        print("begin")
        yield self.db_query()
        self.write("  ffgndjdfjgjff                   hgghk")
        print("end")

app = tornado.web.Application([
         (r"/", MainHandler),
        ])

if __name__ == '__main__':
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()

