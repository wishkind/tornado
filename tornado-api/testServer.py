import os
import tornado.web
import tornado.ioloop
from tornado.options import define, options
define("port", default="8888", help="server port")
settings = {
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
    "cookie_secret": "__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
    "login_url": "/login",
    "xsrf_cookies": True,
}
class MainHandler(tornado.web.RequestHandler):
    def initialize(self):
        #self.set_default_headers()
        pass
    def get(self):
        self.render("index.html")


    def set_default_headers(self):
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Headers', '*')
        self.set_header('Access-Control-Max-Age', 1000)
        self.set_header('Content-type', 'application/json')
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.set_header('Access-Control-Allow-Headers',
                    'Content-Type, Access-Control-Allow-Origin, Access-Control-Allow-Headers, X-Requested-By, Access-Control-Allow-Methods')





app = tornado.web.Application([
     (r'/', MainHandler),
    ],
  )

if __name__ == "__main__":
    options.parse_command_line()
    server = tornado.httpserver.HTTPServer(app)
    server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()    
