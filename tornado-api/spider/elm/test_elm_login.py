import json
import requests
import time


session = requests.session()

mobile = '18368142790'
verifyCode = ''


# 发送手机验证码
def send_code():
    url = 'https://app-api.shop.ele.me/arena/invoke/?method=LoginService.sendVerifyCode'
    data = {
        "id":"1D60002F18364DA29651174CD5713BB4|1545372638212",
        "metas":{
            "appName":"melody",
            "appVersion":"1.1.1"
        },
        "service":"LoginService",
        "method":"sendVerifyCode",
        "params":{
            "mobile": mobile,
            "isByVoice": 'false'
        },
        "ncp":"2.0.0"
    }
    headers = {
        'content-type': 'application/json;charset=UTF-8',
        'origin': 'https://melody.shop.ele.me',
        'referer': 'https://melody.shop.ele.me/login',
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
        'x-eleme-requestid': "1D60002F18364DA29651174CD5713BB4|1545372638212"
    }

    res = session.post(url, data=json.dumps(data), headers=headers)

    print('发送验证码RSE: ', res.text)


# 手机号登录
def login_mobile():
    send_code()
    code = input('等待输入手机验证码: ')

    url = 'https://app-api.shop.ele.me/arena/invoke/?method=LoginService.loginByUsername'
    headers = {
        'content-type': 'application/json;charset=UTF-8',
        'origin': 'https://melody.shop.ele.me',
        'referer': 'https://melody.shop.ele.me/login',
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
        'x-eleme-requestid': "1D60002F18364DA29651174CD5713BB4|1545372638212"
    }
    data = {
        "id": "1D60002F18364DA29651174CD5713BB4|1545372638212",
        "metas": {
            "appName": "melody",
            "appVersion": "1.1.1"
        },
        "service": "RiskLoginService",
        "method": "loginByMobile",
        "params": {
            "mobile": mobile,
            "verifyCode": code,
            "captchaCode": "",
            "loginedSessionIds": []
        },
        "ncp": "2.0.0"
    }

    res = session.post(url, data=json.dumps(data), headers=headers)
    print('手机号登录RES: ', res.text)


def test():
    login_mobile()


if __name__ == '__main__':
    test()
