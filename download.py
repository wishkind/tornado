import tornado
import tornado.web
import tornado.ioloop
import tornado.escape
import tornado.options
from tornado.options import define, options, parse_command_line
import os
import json
import asyncio
import uuid
import tornado.locks
define("port", default=8888, help="run on the given port", type=int)
define("debug", default=True, help="run in debug mode")

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("ggg")
        #self.render("index.html")

class DownloadHandler(tornado.web.RequestHandler):
    def initialize(self, basepath):
        self.database = basepath
        print(basepath)
    def get(self,filename):
        self.set_header('Content-Type', 'application/octet-stream')
        self.set_header('Content-Disposition', 'attachment; filename=%s' % filename)
 
        path = os.path.join(self.basepath,filename)
        with open( path, 'rb') as f:
            while True:
                data = f.read(4096)
                if not data:
                    break
                self.write(data)
 
        self.finish()

class SDownloadHandler(tornado.web.RequestHandler):
    def get(self):
        filename = self.get_argument('filename')
        json_string = {}

        """
        将请求参数放到dict中
        """
        type = self.get_argument('type')
        starttime = self.get_argument('starttime')
        endtime = self.get_argument('endtime')
        json_string['starttime'] = starttime
        json_string['endtime'] = endtime
        json_string['type'] = type
  
        """
        生成json文件
        """
        if json_string:
            filepath = './jsonfile.txt'
            if os.path.exists(filepath):
                os.remove(filepath)
            ff = open(filepath, 'w')
            json.dump(json_string, ff)  # 将json格式数据写入文件
            ff.close()

        """
          下载文件
          """
        filename = "jsonfile.txt"
        self.set_header ('Content-Type', 'application/octet-stream')
        self.set_header ('Content-Disposition', 'attachment; filename=' + filename)
        buf_size = 4096
        with open(os.path.join('',filepath), 'rb') as f:
            while True:
                data = f.read(buf_size)
                if not data:
                    break
                self.write(data)
                self.finish()

class UploadHandler(tornado.web.RequestHandler):
    def initialize(self, upload_path, naming_strategy):
        self.upload_path = upload_path
        if naming_strategy is None:
            naming_strategy = str(uuid_uuid4())
    


    def post(self):
        print(self.request.files.keys()) # [u'want_to_upload_file_1', u'want_to_upload_file_2']
        print(type(self.request.files['want_to_upload_file_1'])) # list,长度为1
        meta_file_1 = self.request.files['want_to_upload_file_1'][0]
        print(meta_file_1.keys()) # ['body', 'content_type', 'filename']
        print(len(meta_file_1['body'])) # 31492，文件长度
        print(meta_file_1['content_type']) # image/jpeg
        print(meta_file_1['filename']) # dqd.jpg
 
        PROJECT_PATH = os.path.split(os.path.realpath(__file__))[0]
        upload_path = os.path.join(PROJECT_PATH, 'static', 'image', 'wiki')
        file_name = os.path.join(upload_path, meta_file_1['filename'])

        with open(file_name, 'wb') as fp:
           fp.write(meta_file_1['body'])
        
        fileinfo = self.request.files['filename'][0]
        filename = fileinfo['filename']
        try:
            with open(os.path.join(self.upload_path, filename), 'w') as f:
                f.write("%s uploaded %s, saved as %s", \

                       str(self.request.remote_ip), \
                       str(fileinfo['filename']), filename)
        except IOError as e:
            logging.error("Failed to write file due to IOError %s", str(e))

def main():
    parse_command_line()
    app = tornado.web.Application([
          (r"/", MainHandler),
          (r"/download", DownloadHandler, dict(download_path="tmp", name_strategy=None)),
          (r"/static(.*)", UploadHandler, dict(basepath="/tmp/static")), 
          (r"/ddd", SDownloadHandler),	
           ],
          cookie_secret="__TODO:_GENERATE__",
          template_path=os.path.join(os.path.dirname(__file__), "templates"),
          static_path=os.path.join(os.path.dirname(__file__), "static"),
         xsrf_cookies=True,
         debug=options.debug,
   )
    app.listen(options.port)
    tornado.ioloop.IOLoop.current().start()

if __name__ == "__main__":
    main()
    
