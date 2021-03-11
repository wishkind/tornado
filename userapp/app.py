from handlers.user import AllUsersHandler
from handlers.user import UserHandler
import tornado.web
import tornado.httpserver
import tornado.ioloop

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("good")


HANDLERS = [
    (r'/', MainHandler),
    (r'/api/user/(\d+)', UserHandler),
    (r'/api/user', AllUsersHandler),
   ]
def run():
    app = tornado.web.Application(
        HANDLERS,
        debug = True
        )
    http_server = tornado.httpserver.HTTPServer(app)
    port = 8888
    http_server.listen(port)
    print('server is start at:{}'.format(port))
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    run()
