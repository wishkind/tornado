"""
A python file server, implemented by Tornado.

Author: Miunchiuan Gao <minchiuan.gao@gmail.com>
Create Date: 2015-Oct-28
"""

import hashlib
import tornado.ioloop
import tornado.web
import os
import imghdr


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        """
        gets a test website to upload file directly.
        """
        self.write(
                """
                <html>
            <head><title>Upload File</title></head>
            <body>
            <form action='file/upload' enctype="multipart/form-data" method='post'>
            <input type='file' name='file'/><br/>
            <input type='submit' value='submit'/>
            </form>
            </body>
            </html>
                """
        )
        

class FileDownloadHandler(tornado.web.RequestHandler):
    def get(self, file_name):
        '''
        downloads the file by file_name
        '''
        down_path = os.path.join(os.path.dirname(__file__), 'files')
        file_path = os.path.join(down_path, file_name)
        if file_name and os.path.exists(file_path):
            self.set_header ('Content-Type', 'application/octet-stream')
            self.set_header ('Content-Disposition', 'attachment; filename=%s' % file_name)
            with open(file_path, 'rb') as f:
                try:
                    while True:
                        _buffer = f.read(1024 * 4)
                        if _buffer:
                            self.write(_buffer)
                        else:
                            f.close()
                            self.finish()
                            return
                except:
                    raise tornado.web.HTTPError(500)
        else:
            raise tornado.web.HTTPError(404)


class FileHandler(tornado.web.RequestHandler):
    def get(self, file_name):
        self.write('upload handler get')


    def post(self):
        # receives a posted file, and saves it.
        conf={}
        upload_path=os.path.join(os.path.dirname(__file__),'files') 
        file_metas = self.request.files['file']
        file_name = None
        for meta in file_metas:
            file_name = meta['filename']
            body = meta['body']
            data = file_name.encode('utf-8') + body
            data_md5 = hashlib.md5(data).hexdigest()
            file_saved_path = os.path.join(upload_path, data_md5)

            with open(file_saved_path, 'wb') as up:
                up.write(body)
            
            file_extension = imghdr.what(file_saved_path)
            os.rename(file_saved_path, file_saved_path + '.' + file_extension)

            conf[file_name] = data_md5 + '.' + file_extension

        self.write(conf)



settings = {
        "static_path": os.path.join(os.path.dirname(__file__), "files"),
        "cookie_secret": "61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
        "login_url": "/login",
        "xsrf_cookies": False,
        }


application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/file/upload", FileHandler),
    (r"/file/(.*)", FileDownloadHandler),
    ], **settings)


if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()

