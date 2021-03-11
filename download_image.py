from abc import ABC
import tornado.web
from tornado.httpclient import HTTPClient
from tornado.httpclient import AsyncHTTPClient
from tornado.web import RequestHandler
from tornado.web import StaticFileHandler
#from libs.hooks import check_token
#from libs.encode import Encode
import time
import io
import os
from PIL import Image
#from settings.config import max_img_size

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("good")
class SyncGrabImageHandler(tornado.web.RequestHandler):
    def get(self):
   
        url = "https://img.ivsky.com/img/tupian/pre/202005/03/banma-001.jpg"

        client = HTTPClient()

        result = client.fetch(url)

        img = result.body

        with open('media/image/1.jpg', 'wb') as f:
            f.write(img)
            f.close()

#class GrabImageHandler(AuthBaseHandler):
class GrabImageHandler(tornado.web.RequestHandler): 
    @tornado.gen.coroutine  
    def get(self):
        url = self.get_argument('url')
        if not url:
            return self.write('no url')

        http_client = AsyncHTTPClient()
        try:
            response = yield http_client.fetch(url, request_timeout=6) 
            print(response)
            with open('media/image/1.jpg', 'wb') as f:
                f.write(response.body)
                f.close()
        except AttributeError as e:
            self.write(e)
class ImageHandler(RequestHandler, ABC):
    async def get(self, *args, **kwargs):
        url = self.request.uri
        if url.startswith("/image/") and url.endswith(".jpg"):
            file_name = 'static/upload/{}'.format(url[7:])
            await self.download(file_name)
            pass
        else:
            self.write("Invalid path ")
            self.write_error(404)

 #   @check_token
    async def post(self):
        url = self.request.uri
        token = self.get_body_argument('token')
        if url.startswith("/image/upload"):
            image = self.get_body_argument('image')
            image_data = Encode.decode(image)
            ut = int(time.time())
            file_name = token + str(ut) + ".jpg"
            save_to = 'static/upload/{}'.format(file_name)
            await self.upload(image_data, save_to)
        self.write_error(404)

    async def download(self, file_name):
        try:
            img = Image.open(file_name)
            height = img.size[1]
            width = img.size[0]
            #while (height > max_img_size) or (width > max_img_size):
             #   height = height//2
              #  width = width//2
               # print(width, height)
            img = img.resize((width, height))
        except FileNotFoundError:
            self.write_error(404)
            return
        bio = io.BytesIO()
        img.save(bio, "PNG")
        self.set_header('Content-Type', 'image/PNG')
        self.write(bio.getvalue())
        pass

    @staticmethod
    async def upload(image_data, save_to):
        with open(save_to, 'wb') as f:
            f.write(image_data)



    async def download(self, file_name):
        try:
            pic = open(file_name, "rb")
        except FileNotFoundError:
            self.write_error(404)
            return
        self.write(pic.read())
        self.set_header('Content-Type', 'image/png')
        pass


app = tornado.web.Application([
    (r'/', MainHandler),
    (r'/sync', SyncGrabImageHandler),
    (r'/async', GrabImageHandler),
    (r'/image/(.*)', StaticFileHandler,
         {"path": os.path.join(os.path.dirname(__file__), "../static/download"),
          "default_name": "default.jpg"}),
    ])
app.listen(8888)
tornado.ioloop.IOLoop.current().start()
