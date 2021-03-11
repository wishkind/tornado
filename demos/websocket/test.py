#!/usr/bin/env python
import tornado
import tornado.escape
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.websocket
import os.path
import uuid
import os
import logging
from tornado.options import define, options
define("port", default=8888, help="run on the given port", type=int)
class Application(tornado.web.Application):
    def __init(self):
        handlers = [
                      (r"/", MainHandler),
                      (r"/chat", ChatHandler)
                   ]
        settings = dict(
           cookie_secret="__TODO:_GENERATE_YOUR_RANDOM_VALUE_HERE__",
           template_path=os.path.join(os.path.dirname(__file__), "templates"),
           static_path=os.path.join(os.path.dirname(__file__), "static"),
           xsrf_cookies=True,
           )
        super().__init__(handlers, **settings)

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html", messages=ChatHandler.cache)
        self.write("gg")
class ChatHandler(tornado.websocket.WebSocketHandler):
    waiters = set()
    cache = []
    cache_size = 200
    
    def get_compression_options(self):
        return {}

    def open(self):
        ChatHandler.waiters.add(self)

    def on_close(self):
        ChatHandler.waiters.remove(self)

    @classmethod
    def update_cache(cls, chat):
        cls.cache.append(chat)
        if len(cls.cache) > cls.cache_size:
            cls.cache = cls.cache[-cls.cache_size:]
    @classmethod
    def send_updates(cls, chat):
        logging.info("sending message to %d waiters", len(cls.waiters))
        for waiter in cls.waiters:
            try:
                waiter.write_message(chat)
            except:
                logging.error("Error sending message", exc_info=True)

    def on_message(self, message):
        logging.info("got message %r", message)
        parsed = tornado.escape.json_decode(message)
        chat = {"id": str(uuid.uuid4()), "body": parsed["body"]}
        chat["html"] = tornado.escape.to_basestring(
             self.render_string("message.html", message=chat)
        )
        ChatHandler.update_cache(chat)
        ChatHandler.send_updates(chat)

         
def main():
    tornado.options.parse_command_line()
    print(options.port)
    app = Application()
    app.listen(options.port)
    tornado.ioloop.IOLoop.current().start()
if __name__ == "__main__":
    main()
    
