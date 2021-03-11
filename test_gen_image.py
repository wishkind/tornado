<<<<<<< HEAD
#import tornado.web
#import tornado.httpserver
#import tornado.gen
#import tornado.ioloop
#import tornado.httpclient
#import urllib.urlencode
=======
import tornado.web
import tornado.httpserver
import tornado.gen
import tornado.ioloop
import tornado.httpclient
import urllib.urlencode
>>>>>>> third commit

@router.Route('api/v2/account/upload')
class ApiAccountUploadHandler(helper.BaseHandler):
    @tornado.gen.coroutine
    @helper.token_require
    def post(self, *args, **kwargs):
        upload_type = self.get_argument('type', None)
        files_body = self.request.files['file']
        new_file = 'upload/new_pic.jpg'
        new_file_name = 'new_pic.jpg'
      
        #write file
        with open(new_file, 'w') as f:
            f.write(file_['body'])
            f.close()
        logging.info('user {} upload {}'.format(user_id, new_file_name))
        #async request upload image
        with open(new_file, 'rb') as f:
            files = [('image', new_file_name, f.read())]
            fields = (('api_key', KEY), ('api_secret', SECRET))
            content_type, body = encode_multipart_formdata(fields, files)
            headers = {"Content-Type": content_type, "content-length": str(len(body))}
            request = tornado.httpclient.HTTPRequest(config.OCR_HOST, method="POST",
		 headers=headers, body=body, validate_cert=False)
            response = yield tornado.httpclient.AsyncHTTPClient().fetch(request)


def encode_multipart_formdata(fields, files):
    boundary = '----------ThIs_Is_tHE_bouNdaRY_$'
    crlf = '\r\n'
    l = []
    for (key, value) in fields:
        l.append('--' + boundary)
        l.append('Content-Disposition: form-data; name="%s"' % key)
        l.append('')
        l.append(value)
    for (key, filename, value) in files:
        filename = filename.encode("utf-8")
        l.append('--' + boundary)
        l.append('Content-Disposition: form-data; name="%s"; filename="%s"' % (key, filename))
        l.append('Content-Type:%s' % get_content_type(filename))
        l.append('')
        l.append(value)
    l.append('--' + boundary + '--')
    l.append('')
    body = crlf.join(l)
    content_type = 'multipart/form-data; boundary=%s' % boundary
    return content_type, body

def get_content_type(filename):
    import mimetypes
    return mimetypes.guess_type(filename)[0] or 'application/octet-stream'
