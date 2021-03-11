from datetime import datetime
from urllib.parse import urlencode
import time
import random
import zlib
import requests
import json
from spider.meituan.js import *
import base64


class Base(object):
    def getTime(self):
        d1 = datetime(1970, 1, 1)
        d2 = datetime.now()
        d3 = int((d2 - d1).total_seconds() * 1000)
        return d3

    def url_encode(self, data):
        """token解码"""
        if isinstance(data, str):
            data = data.replace(" ", "").encode()
            base_data = zlib.compress(data)
            data = base64.b64encode(base_data)
            return data
        else:
            data = str(data)
            return self.url_encode(data)

    def url_decode(self, data):
        """token编码"""
        if isinstance(data, str):
            data = base64.b64decode(data)
            base_data = zlib.decompress(data)
            return base_data


class Crawl(Base):
    def __init__(self, randomId=None, request_code=None):
        self.request_code = request_code
        self.randomId = '0.8481614070215833'
        self.headers = {
            # 'Accept': '*/*',
            # 'Accept-Encoding': 'gzip, deflate, br',
            # 'Accept-Language': 'zh-CN,zh;q=0.9',
            # 'Connection': 'keep-alive',
            # 'Content-Length': '1695',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Host': 'verify.meituan.com',
            'Origin': 'https://verify.meituan.com',
        }
        self.ts = self.getTime()
        self.cts = self.getTime() + 1000

    def get_img_sign(self):
        token = {}
        token["action"] = '555'
        token["randomId"] = '{}'.format("1,71")
        token["request_code"] ='{}'.format(self.request_code)
        sign = "\"captchacode={}&id={}&request_code={}\"".format(token['action'], token["randomId"],  token["request_code"])
        return sign

    def get_pic_sign(self):
        token = {}
        token["action"] = 'spiderindefence'
        token["randomId"] = '{}'.format(self.randomId)
        token["request_code"] = '{}'.format(self.request_code)
        sign = "\"action={}&randomId={}&request_code={}\"".format(token['action'], token["randomId"],
                                                                  token["request_code"])
        return sign

    def kT(self):
        kt=[]
        for times in range(5):
            time.sleep(0.2)
            i = self.getTime() - self.ts
            s = random.randint(65, 90)
            r = chr(s)
            kt.append("{},INPUT,{}".format(r,i))
        return  kt

    def aT(self):
        at = []
        for times in range(5):
            page_x=random.randint(482, 1283)
            page_y=random.randint(245, 295)
            i = self.getTime() - self.ts
            s = random.choice(['BUTTON','INPUT','DIV'])
            at.append("{},{},{},{}".format(page_x, page_y,s,i))
        return at

    def mT(self):
        at = []

        k = random.randint(40, 60)
        for times in range(60):
            import time
            time.sleep(0.05)
            page_x = random.randint(482, 1283)
            page_y = random.randint(245, 295)
            i = self.getTime() - self.ts
            s = random.choice(['BUTTON', 'INPUT', 'DIV'])
            at.append("{},{},{},{}".format(page_x, page_y, s, i))
        return at

    def img_token(self, request_code):
        sign = self.url_encode(self.get_img_sign()).decode()
        token={
            "ver": "1.0.6",
            "rId": "100019",
            "ts": self.ts,
            "cts": self.cts,
            "brVD": [748, 938],
            "brR": [[1920, 1080], [1920, 1040], 24, 24],
            "bI": ["https://verify.meituan.com/v2/web/general_page?action=spiderindefence&requestCode={}&platform=1000&adaptor=auto&succCallbackUrl=https%3A%2F%2Foptimus-mtsi.meituan.com%2Foptimus%2FverifyResult%3ForiginUrl%3Dhttp%253A%252F%252Fwww.dianping.com%252Fbeijing%252Fch10%252Fg1338&theme=dianping".format(request_code),
                ""],
            "mT": self.mT(),
            "kT": self.kT(),
            "aT": self.aT(),
            "tT": [],
            "aM":'',
            "inputs": [
                {
                    "inputName": "yodaImgCodeInput",
                    "editStartedTimeStamp": self.ts,
                    "keyboardEvent": "0-3-1-7|297",
                    "editFinishedTimeStamp": self.cts
                }
            ],
            "buttons": [
                {
                    "buttonName": "yodaImgCodeSure",
                    "touchPoint": "{498,324}",
                    "touchPosition": "{41,37.1}",
                    "touchTimeStamp": self.ts
                },
                {
                    "buttonName": "yodaNextImgCode",
                    "touchPoint": "{606,261}",
                    "touchPosition": "{42.5,66.6}",
                    "touchTimeStamp":  self.ts
                }
            ],
            "broP": ["Chrome PDF Plugin", "Chrome PDF Viewer", "Native Client"],
            "sign": sign
        }
        return token

    def dowun_pic(self, request_code):
        token = self.url_encode(json.dumps(self.img_token(request_code))).decode()
        base_url='https://verify.meituan.com/v2/captcha?'
        params={
            'request_code': '{}'.format(request_code),
            'action': 'spiderindefence',
            'randomId': '{}'.format(self.randomId),
            '_token': token
        }
        imgurl = base_url + urlencode(params)
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36',
                 'Host': 'verify.meituan.com',
                 'Referer': 'https://verify.meituan.com/v2/web/general_page?action=spiderindefence&requestCode=e741edb57091473abac8e11fc8188c34&platform=1000&adaptor=auto&succCallbackUrl=https%3A%2F%2Foptimus-mtsi.meituan.com%2Foptimus%2FverifyResult%3ForiginUrl%3Dhttp%253A%252F%252Fwww.dianping.com%252Fshanghai%252Fch10&theme=dianping'
                 }
        html = requests.get(imgurl,headers=headers)
        with open('picture.jpg', 'wb') as file:
            file.write(html.content)
        print("自动输入验证码：")
        text = self.discern()
        print(text)
        if self.post_img(img_data=text,request_code=request_code):
            return True

    def discern(self):
        global codetype
        username = 'yangsensheng'
        password = 'yang147258369'
        appid = 3129
        appkey = '40d5ad41c047179fc797631e3b9c3025'
        codetype = 4006
        timeout = 60
        filename = 'picture.jpg'
        if (username == 'username'):
            print('请设置好相关参数再测试')
        else:
            yundama = YDMHttp(username, password, appid, appkey)
            text = yundama.decode(filename, codetype, timeout)

            if text != '':
                return text
            else:
                codetype = 5000
                return self.discern()

    def post_img(self, img_data, request_code):
        url='https://verify.meituan.com/v2/ext_api/spiderindefence/verify?id=1'
        token = self.url_encode(json.dumps(self.img_token(request_code))).decode()
        data = {
            'id': '71',
            'request_code': '{}'.format(request_code),
            'captchacode':img_data,
            '_token':token,
        }

        r = requests.post(url,headers=self.headers,data=data)
        response = r.json()
        if response.get('status') == 1:
            print("验证成功")
            return True
        else:
            message = response.get('error')['message']
            if message == "验证码不正确，请重新输入":
                print(message)
                return self.dowun_pic(request_code)
            elif message == "授权码已过期，请退出验证页面，重新操作":
                print(message)
                return False
            else:
                print(message)
                if self.slider_(request_code):
                    print("验证成功")
                    return True

    def point(self):
        trace = []
        k = random.randint(5, 20)
        for i in range(k):
            F = random.randint(400 + i * 30, 400 + (i + 1) * 30)
            S = random.randint(250 + i * 10, 250 + (i + 1) * 10)
            T = random.randint(1000 + i * 100, 1000 + (i + 1) * 100)
            k = [0, F, S, T]
            trace.append(k)
        return trace

    def behavior(self, request_code):
        t = base_(request_code)
        trace = self.point()
        e = '{"env":{"zone":[230,33],"client":[391,243.5],"Timestamp":[%d,%d],"count":1,"timeout":0},"trajectory":[{"point":%s}]}' % (self.ts, self.cts, trace)
        s = ctx.call('f', e, t)
        behavior = ctx.call('o',s)
        return behavior

    def slider_token(self, request_code):
        be_ = 'behavior={}{}'.format(self.behavior(request_code), '&fingerprint=undefined&id=71&request_code={}'.format(self.request_code))
        sign = self.url_encode(json.dumps(be_)).decode()
        print('sign: ', sign)
        token = {
            "ver": "1.0.6",
            "rId": "100019",
            "ts": self.ts,
            "cts": self.cts,
            "brVD": [800, 600],
            "brR": [[1920, 1080], [1858, 1080], 24, 24],
            "bI": [
                "https://epassport.meituan.com/account/unitivelogin?bg_source=3&service=waimai&platform=2&continue=http://e.waimai.meituan.com/v2/epassport/entry&left_bottom_link=%2Faccount%2Funitivesignup%3Fbg_source%3D3%26service%3Dwaimai%26platform%3D2%26continue%3Dhttp%3A%2F%2Fe.waimai.meituan.com%2Fv2%2Fepassport%2FsignUp%26extChannel%3Dwaimaie%26ext_sign_up_channel%3Dwaimaie&right_bottom_link=%2Faccount%2Funitiverecover%3Fbg_source%3D3%26service%3Dwaimai%26platform%3D2%26continue%3Dhttp%3A%2F%2Fe.waimai.meituan.com%2Fv2%2Fepassport%2FchangePwd",
                "http://e.waimai.meituan.com/logon/error/1001"
            ],
            "mT": self.mT(),
            "kT": [],
            "aT": self.aT(),
            "tT": [],
            "aM": "",
            "inputs": [],
            "buttons": [{'buttonName': "rohr_179692", 'touchPoint': "{416,235}", 'touchPosition': "{55.7,60.5}", 'touchTimeStamp': int(time.time() * 1000)}],
            "broP": ["Chrome PDF Plugin", "Chrome PDF Viewer", "Native Client"],
            "sign": sign
        }

        return token

    def slider_(self, request_code):
        data_token = self.slider_token(request_code)

        token = self.url_encode(json.dumps(data_token)).decode()

        print('data_token: ', data_token)
        print('token: ', token)
        print('self.behavior(request_code): ', self.behavior(request_code))

        url = 'https://verify.meituan.com/v2/ext_api/spiderindefence/verify?id=71'

        data = {
            'request_code': request_code,
            'behavior': self.behavior(request_code),
            'fingerprint': 'undefined',
            '_token': token
        }

        r = requests.post(url, headers=self.headers, data=data)
        response = r.text
        response = json.loads(response)
        print('response: ', response)
        exit()
        try:
            if response['status'] == 1:
                print('print("滑块通过")')
                return True
            else:
                error = response['error']
                message = error['message']
                if message == '需要验证图片验证码':
                    print(message)
                    img_code = error['request_code']
                    print(img_code)
                    if self.dowun_pic(img_code):
                        print("滑块通过")
                        return True

                elif message == '授权码已过期，请退出验证页面，重新操作':
                    print(message)
                    return False

                elif  message == '请求异常,拒绝操作':
                    print(message)
                    return False

                else:
                    if self.dowun_pic(request_code):
                        return True

        except Exception as e:
            print(e)


if __name__ == '__main__':
    # request_code = input('request_code: ')
    request_code = 'e2f5d0acfad94c0b90a79aad1a89ad3c'
    spider = Crawl()
    spider.slider_(request_code)
    # a = spider.point()
