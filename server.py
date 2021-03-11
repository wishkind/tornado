# -*- coding: utf-8 -*-

import cv2
import random
import os.path
import tornado.web
import tornado.ioloop
import tornado.options
import tornado.httpserver
from tornado.options import define, options
from PIL import Image
import io
import matplotlib.pyplot as plt
from peewee import *
import peewee_async
import asyncio

from datetime import datetime
# 保存图片
def tag_picture(imagepath, name):
    print(imagepath)
    image = cv2.imread(imagepath, 1)
    #img = Image.open(imagepath)
    #img.show()
    new_path = os.path.dirname(os.path.abspath(__file__)) + '/new_images/'
    os.makedirs(new_path, exist_ok=True)
    new_filename = os.path.join(new_path, name + '.png')
    print(new_filename)
    cv2.imwrite(new_filename, image)

#定义端口为8888
define("port", default=9000, type=int)

# 随机获取目录下的一张图片
def get_image(dir):
    files = os.listdir(dir)
    return random.choice(files)



database = peewee_async.PostgresqlDatabase(
        database ='postgres',
        user='postgres',
        password = 'dragon',
        host='127.0.0.1',
        port='5432'
)
loop = asyncio.get_event_loop()
 
class BaseModel(Model):
    add_time = DateTimeField(default=datetime.now, verbose_name="添加时间", help_text='添加时间')
    update_time = DateTimeField(default=datetime.now, verbose_name='更新时间', help_text='更新时间')

    def save(self, *args, **kwargs):
        if self._get_pk_value() is None:
            self.add_time = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S")
        self.update_time = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S")

        return super(BaseModel, self).save(*args, **kwargs)



class MainHandler(tornado.web.RequestHandler):
    def initialize(self):
        self.set_default_headers()
    def get(self):
        dir = './static/images'
        files = os.listdir(dir)
        img_src = files[0]
        print(img_src)
        #self.write({"name":"hello"})
        self.render("index.html", img_src=img_src, imgname=img_src)
    def post(self):
        
        print(self.request.method)
        filename = self.get_argument("rename")
        print("filename=", filename)
        imgname = self.get_argument('imgname')
        print("image=", imgname)
        imagepath = os.path.dirname(os.path.abspath(__file__))+'/static/images/%s' % imgname
        tag_picture(imagepath, filename)            # 保存新图片
        #os.system('rm -rf %s' % imagepath)          # 删除原图片
        print(len(os.listdir('./static/images')))   # 剩余图片数量

        dir = './static/images'
        img_src = get_image(dir)
        self.render('index.html', img_src=img_src, imgname=img_src)  

    def set_default_headers(self):
        print("set default header")
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Headers', '*')
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')      






class ImageHandler(tornado.web.RequestHandler):
    def initialize(self):
        # self.request.method = 'POST'
        # print(self.request.method, type(self.request.method))
        self.set_default_header()

    # get函数
    def get(self):
        dir = './static/images'
        img_src = get_image(dir)
        self.render('index.html', img_src=img_src, imgname=img_src)
    # post函数
    def post(self):
        print("post")
        filename = self.get_argument('rename')
        print("filename=", filename)
        imgname = self.get_argument('imgname')
        print("image=", imgname)
        imagepath = os.path.dirname(__file__)+'/static/images/%s' % imgname
        tag_picture(imagepath, filename)            # 保存新图片
        os.system('rm -rf %s' % imagepath)          # 删除原图片
        print(len(os.listdir('./static/images')))   # 剩余图片数量

        dir = './static/images'
        img_src = get_image(dir)
        self.render('index.html', img_src=img_src, imgname=img_src)

    def set_default_headers(self):
        print('set headers!!')
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Headers', '*')
        self.set_header('Access-Control-Max-Age', 1000)
        self.set_header('Content-type', 'application/json')
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.set_header('Access-Control-Allow-Headers',
                    'Content-Type, Access-Control-Allow-Origin, Access-Control-Allow-Headers, X-Requested-By, Access-Control-Allow-Methods')

    def OPTIONS(self):
        pass
    def PUT(self):
        pass
    def DELETE(self):
        pass
    def TRACE(self):
        pass

class AsyncTextHandler(tornado.web.RequestHandler):
    async def get(self, *args, **kwargs):
        try: 
            f = open("./static/texts/quiz.json")
        except FileNotFoundError:
            print("file not exist") 
            self.write_error(404)
            return    
        bio = io.BytesIO()
        f.save(bio, "txt")
        self.set_header("Content-Type", "application/json")
        self.write(bio.getvalue()) 
class AsyncImageHandler(tornado.web.RequestHandler):
    async def get(self, *args, **kwargs):
        url = self.request.uri
        file_name = './static/images/1.jpg'
        await self.download(file_name)
        pass

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

# 主函数
def main():

    tornado.options.parse_command_line()
    app = tornado.web.Application([
               (r'/', MainHandler),
               (r'/async', AsyncImageHandler),
               (r'/image', ImageHandler),
               (r'/text', AsyncTextHandler),    
            ],    
            template_path=os.path.join(os.path.dirname(__file__), "templates"), 
            static_path=os.path.join(os.path.dirname(__file__), "static"),                )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

main()
