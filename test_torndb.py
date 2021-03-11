import pymysql.connections
import pymysql.converters
import pymysql.cursors
pymysql.install_as_MySQLdb()
import MySQLdb
import tornado
import tornado.ioloop
import tornado.web
import tornado.httpserver
from tornado.options import options, define
define("port", default=8888, type=int)
class IndexHandler(tornado.web.RequestHandler):
  def get(self, *args, **kwargs):
    self.write('write')


if __name__ == '__main__':
  options.parse_command_line()
  app = tornado.web.Application([
     (r'/', IndexHandler),
     ], 
     debug=True)


  http_server = tornado.httpserver.HTTPServer(app)
  http_server.listen(options.port)
  tornado.ioloop.IOLoop.current().start()

