# import js2py
import random

import execjs
import requests, zlib, base64, json
from datetime import datetime


def c(e, t):
    n = len(e)
    r = n >> 2
    if t:
        r = r + 2
    i = [0 * i for i in range(r)]
    for o in range(n):
        i[o >> 2] |= ord(e[o]) << ((o & 3) << 3)
    if t:
        i[-1] = n
    return i


def base_(a):
    return base64.b64encode(a.encode()).decode().replace('=', ")")


ctx = execjs.compile("""
 function f(e, t) {
            return b(r(e, t))
        }
   function r(e, t) {
   return  a(v(c(e, true), s(c(t, false))))

        }
       function s(e) {
            return e["length"] < 4 && (e["length"] = 4),
            e
        }
 function c(e, t) {
            var n = e["length"]
              , r = n >> 2;
            (n & 3) !== 0 && ++r;
            var i;
            t ? (i = new Array(r + 1),
            i[r] = n) : i = new Array(r);
            for (var o = 0; o < n; ++o)
                i[o >> 2] |= e["charCodeAt"](o) << ((o & 3) << 3);
            return i
        }


function v(e, t) {
            var n, r, i, o, a, c, s = e["length"], u = s - 1;
            for (r = e[u],
            i = 0,
            c = Math.floor(6 + 52 / s) | 0; c > 0; --c) {
                for (i = i + 2654435769 & 4294967295,
                o = i >>> 2 & 3,
                a = 0; a < u; ++a)
                    n = e[a + 1],
                    r = e[a] = e[a] + ((r >>> 5 ^ n << 2) + (n >>> 3 ^ r << 4) ^ (i ^ n) + (t[a & 3 ^ o] ^ r)) & 4294967295;
                n = e[0],
                r = e[u] = e[u] + ((r >>>5 ^ n << 2) + (n >>> 3 ^ r << 4) ^ (i ^ n) + (t[u & 3 ^ o] ^ r)) & 4294967295
            }
            return e
}

function a(e, t) {
            var n = e["length"]
              , r = n << 2;
            if (t) {
                var i = e[n - 1];
                if (r -= 4,
                i < r - 3 || i > r)
                    return Sr;
                r = i
            }
            for (var o = 0; o < n; o++)
                e[o] = String["fromCharCode"](e[o] & 255, e[o] >>> 8 & 255, e[o] >>> 16 & 255, e[o] >>> 24 & 255);
            var a = e["join"]("");
            return t ? a["substring"](0, r) : a
        }
var b = function() {
            var e = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "+", "/"];
            return function(t) {
                var n, r, i, o, a, c, s;
                for (r = i = 0,
                o = t["length"],
                a = o % 3,
                o -= a,
                c = o / 3 << 2,
                a > 0&& (c += 4),
                n = new Array(c); r < o; )
                    s = t["charCodeAt"](r++) << 16 | t["charCodeAt"](r++) << 8 | t["charCodeAt"](r++),
                    n[i++] = e[s >> 18] + e[s >> 12 & 63] + e[s >> 6 & 63] + e[s & 63];
                return a == 1 ? (s = t["charCodeAt"](r++),
                n[i++] = e[s >> 2] + e[(s & 3) << 4] + "==") : a == 2 && (s = t["charCodeAt"](r++) << 8 | t["charCodeAt"](r++),
                n[i++] = e[s >> 10] + e[s >> 4 & 63] + e[(s & 15) << 2] + "="),
                n["join"]("")
            }
        }()
 function o(e) {
            for (var t = "/", n = "+", r = e["split"](""), i = [], o = 0; o < r["length"]; o++) {
                var a = r[o];
                a === "/" && (a = "("),
                a === n && (a = ")"),
                i["push"](a)
            }
            return i["reverse"]()["join"]("")
        }


""")


class Crawl(object):
    def __init__(self, request_code):
        self.request_code = request_code
        self.headers = {
            'Accept': '*/*',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Host': 'verify.meituan.com',
            'Origin': 'https://epassport.meituan.com',
            'Referer': 'https://epassport.meituan.com/account/unitivelogin?bg_source=3&service=waimai&platform=2&continue=http://e.waimai.meituan.com/v2/epassport/entry&left_bottom_link=%2Faccount%2Funitivesignup%3Fbg_source%3D3%26service%3Dwaimai%26platform%3D2%26continue%3Dhttp%3A%2F%2Fe.waimai.meituan.com%2Fv2%2Fepassport%2FsignUp%26extChannel%3Dwaimaie%26ext_sign_up_channel%3Dwaimaie&right_bottom_link=%2Faccount%2Funitiverecover%3Fbg_source%3D3%26service%3Dwaimai%26platform%3D2%26continue%3Dhttp%3A%2F%2Fe.waimai.meituan.com%2Fv2%2Fepassport%2FchangePwd',
            # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36',
        }
        self.ts = self.getTime()
        self.cts = self.getTime() + 1000

    def mT(self):
        at = []
        k = random.randint(40, 60)
        for times in range(k):
            import time
            time.sleep(0.05)
            page_x = random.randint(482, 1283)
            page_y = random.randint(245, 295)
            i = self.getTime() - self.ts
            s = random.choice(['BUTTON', 'INPUT', 'DIV'])
            at.append("{},{},{},{}".format(page_x, page_y, s, i))
        return at

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

    def get_token(self):
        be_ = 'behavior={}{}'.format(self.behavior(), '&fingerprint=undefined&id=71&request_code={}'.format(self.request_code))
        sign = self.url_encode(json.dumps(be_)).decode()
        token = {
            "ver": "1.0.6",
            "rId": "100019",
            "ts": 1544597858984,
            "cts": 1544597977143,
            "brVD": [533, 938],
            "brR": [[1920, 1080], [1920, 1040], 24, 24],
            "bI": [
                "https://epassport.meituan.com/account/unitivelogin?bg_source=3&service=waimai&platform=2&continue=http://e.waimai.meituan.com/v2/epassport/entry&left_bottom_link=%2Faccount%2Funitivesignup%3Fbg_source%3D3%26service%3Dwaimai%26platform%3D2%26continue%3Dhttp%3A%2F%2Fe.waimai.meituan.com%2Fv2%2Fepassport%2FsignUp%26extChannel%3Dwaimaie%26ext_sign_up_channel%3Dwaimaie&right_bottom_link=%2Faccount%2Funitiverecover%3Fbg_source%3D3%26service%3Dwaimai%26platform%3D2%26continue%3Dhttp%3A%2F%2Fe.waimai.meituan.com%2Fv2%2Fepassport%2FchangePwd",
                "http://e.waimai.meituan.com/logon"
            ],
            "mT": ["498,187","495,187","494,187","493,187","492,187","490,187","488,187","487,187","486,187","482,187","480,186","477,186","476,186","475,186","474,186","471,186","470,186","469,186","468,186","465,186","464,186","461,184","459,184","458,184","456,184","455,184","451,184","449,184","442,184","437,184"],
            "kT": [], "aT": [], "tT": [], "aM": "", "inputs": [],
            "buttons": [],
            "broP": ["Chrome PDF Plugin", "Chrome PDF Viewer", "Native Client"],
            "sign": sign
        }
        return token

    def behavior(self):
        t = base_(self.request_code)
        e = {"env":{"zone":[230,33],"client":[286,172],"Timestamp":[1545045351831,1545045356402],"count":1,"timeout":0},
             "trajectory":[{"point":[[0,299,188,4571],[0,309,187,4709],[0,313,184,4726],[0,315,184,4743],[0,316,184,4759],
                                     [0,319,184,4774],[0,323,184,4793],[0,330,184,4809],[0,337,184,4826],[0,348,184,4842],
                                     [0,351,184,4859],[0,354,184,4876],[0,355,184,4893],[0,359,184,4909],[0,360,184,4926],
                                     [0,362,184,4942],[0,365,184,4959],[0,367,184,4976],[0,371,184,4993],[0,378,184,5009],
                                     [0,387,184,5026],[0,395,184,5042],[0,400,184,5059],[0,402,184,5075],[0,405,184,5093],
                                     [0,406,184,5110],[0,407,184,5130],[0,411,184,5143],[0,413,184,5159],[0,415,184,5176],
                                     [0,420,184,5193],[0,421,184,5209],[0,425,184,5226],[0,430,184,5242],[0,432,184,5259],
                                     [0,437,184,5275],[0,442,184,5292],[0,449,184,5309],[0,451,184,5325],[0,455,184,5342],
                                     [0,456,184,5361],[0,458,184,5386],[0,459,184,5393],[0,461,184,5410],[0,464,186,5426],
                                     [0,465,186,5443],[0,468,186,5465],[0,469,186,5476],[0,470,186,5492],[0,471,186,5509],
                                     [0,474,186,5526],[0,475,186,5545],[0,476,186,5559],[0,477,186,5576],[0,480,186,5593],
                                     [0,482,187,5609],[0,486,187,5626],[0,487,187,5642],[0,488,187,5659],[0,490,187,5682],
                                     [0,492,187,5725],[0,493,187,5777],[0,494,187,5801],[0,495,187,5817],[0,498,187,5874]]}]}
        s = ctx.call('f', e, t)
        behavior = ctx.call('o', s)
        print('behavior: ', behavior)
        return behavior

    def splider_(self):
        data_token = self.get_token()
        token = self.url_encode(json.dumps(data_token)).decode()
        url = 'https://verify.meituan.com/v2/ext_api/merchantlogin/verify?id=71'
        data = {
            'request_code': self.request_code,
            'behavior': self.behavior(),
            'fingerprint': 'undefined',
            '_token': token
        }
        print('data: ', data)
        r = requests.post(url, headers=self.headers, data=data)
        print(r.json())


if __name__ == '__main__':
    requests_code = '596de946b12d0516b3a68302'
    splider = Crawl(requests_code)
    splider.splider_()




