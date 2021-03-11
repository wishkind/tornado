import sys

from tornado import web, ioloop
import tornado.web
import tornado.ioloop
from tornado.options import define, options
import tornado.escape
import tornado.httpserver
from peewee_async import Manager
import wtforms_json

from blog.urls import url_pattern
from blog.settings import settings, database
define("port", default="8888", help="server port")

def main():

    wtforms_json.init()

    app = tornado.web.Application(url_pattern, debug=True, **settings)
    app.listen(port)

    objects = Manager(database)
    database.set_allow_sync(False)
    app.objects = objects

    print(f'start server Success! {port}')

    tornado.ioloop.IOLoop.current().start()


if __name__ == '__main__':
    main()
