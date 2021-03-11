import os
import tornado.web
import tornado.ioloop
import tornado.gen
from tornado.options import define, options
current_path = '/'
define("port", default="8888", help="listen port")
class MainHandler(tornado.web.RequestHandler):
    def initialize(self):
        self.set_default_headers()
    def get(self):
        self.render("index.html")

    def set_default_headers(self):
        print("set default header")
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Headers', '*')
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

class DemoHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("010-default.html")






app = tornado.web.Application([
    (r'/', MainHandler),
    (r'/demo', DemoHandler),
    #(r'^/()$', StaticFileHandler, {"path":os.path.join(current_path, "statics/html"), "default_filename":"index.html"}),
    #(r'^/view/(.*)$', StaticFileHandler, {"path":os.path.join(current_path, "statics/html")}),
  ],
  static_path=os.path.join(os.path.dirname(__file__), "statics"),
  #template_path=os.path.join(os.path.dirname(__file__), "templates"),
  )


if __name__ == '__main__':
  tornado.options.parse_command_line()
  server = tornado.httpserver.HTTPServer(app)
  server.listen(options.port)
  tornado.ioloop.IOLoop.current().start()
