import tornado.web
import tornado.ioloop
import tornado.httpserver
import tornado.options
import os 
import spider.tv.tencent
import spider.tv.aiqiyi
  
import spider.movie.tencent
import spider.movie.aiqiyi
 
import spider.variety.tencent
import spider.variety.aiqiyi
 
from tornado.options import options
from tornado.web import RequestHandler, StaticFileHandler

tornado.options.define("port", type=int, default=8888, help="服务器端口")


class IndexHandler(RequestHandler):
 
    # 主页处理类
    def get(self):
        self.render("index.html")

    def post(self):
        self.render("index.html")
 
 
class TvHandler(RequestHandler):
    def post(self):
        name = self.get_argument("name")
        type = self.get_argument("type")
        if type == '1':
            resultTencent = spider.tv.tencent.tencents(self, name)
            resultAiqiyi = spider.tv.aiqiyi.aiqiyi(self, name)
            data = {
                 "tencent": resultTencent,
                 "aiqiyi": resultAiqiyi,
                }
            self.write(data)
        elif type == '2':
            resultTencent = spider.movie.tencent.tencents(self, name)
            resultAiqiyi = spider.movie.aiqiyi.aiqiyi(self, name)
            data = {
                  "tencent": resultTencent,
                  "aiqiyi": resultAiqiyi,
              }
            self.write(data)
        elif type == '3':
            resultTencent = spider.variety.tencent.tencents(self, name)
            resultAiqiyi = spider.variety.aiqiyi.aiqiyi(self, name)
            data = {
                "tencent": resultTencent,
                "aiqiyi": resultAiqiyi,
              }
            self.write(data)

 
if __name__ == '__main__':
    tornado.options.parse_command_line()
    current_path = os.path.dirname(__file__)
    app = tornado.web.Application([
              (r'/', IndexHandler),
              (r'/api/tv', TvHandler),
              (r'/(.*)', StaticFileHandler, {
                 "path": os.path.join(current_path, "statics/html"),
                 "default_filename": "index.html"
                 }),
          ],
         static_path=os.path.join(current_path, "static"),
         template_path=os.path.join(current_path, "template"),
         debug=True,
         autoescape=None
      )
 
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()



from urllib import request, parse
from lxml import etree
import ssl
  
# 取消 https 代理验证
ssl._create_default_https_context = ssl._create_unverified_context
  
 
def aiqiyi(self, name):     
    # 报头
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36'
    headers = {'User-Agent': user_agent}
    url = "https://so.iqiyi.com/so/q_" + parse.quote(name)
    req = request.Request(url, headers=headers)
    try:
        response = request.urlopen(req)
        # 获取每页的HTML源码字符串
        html = response.read().decode('utf-8')
        # 解析html 为 HTML 文档
        selector = etree.HTML(html)

        # 来源
        source = "爱奇艺视频"

         # 剧照
        pic = 'https:' + \
             selector.xpath('//ul[@class="mod_result_list"]/li[1]/a//img/@src')[0]

        # 导演
        director = selector.xpath(
             "//ul[@class='mod_result_list']/li[1]//div[@class='info_item'][1]/div[@class='result_info_cont result_info_cont-half'][1]/a[@class='result_info_link']/text()")
         # 主演 
        actor = selector.xpath(
             "//ul[@class='mod_result_list']/li[1]//div[@class='info_item'][1]/div[@class='result_info_cont result_info_cont-half'][2]/a[@class='result_info_link']/text()")
 
         # 简介
        desc = selector.xpath(
           "//ul[@class='mod_result_list']/li[@class='list_item'][1]//div[@class='info_item'][2]//span[@class='result_info_txt']/text()")[
            0]
 
         # 链接
        link = selector.xpath('//ul[@class="mod_result_list"]/li[1]/a/@href')[0]
        defalut_result = {
            "source": source,
             "name": name,
             "pic": pic,
             "director": director,
             "actor": actor,
             "desc": desc,
             "list": [{'title': '播放', 'link': link}]
            }
        return defalut_result  
    except Exception:
        print(url, Exception)
        data = {"code": -1, "message": "error", "data": None}
        return data
