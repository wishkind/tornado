import base64
import json
import random
import zlib

import requests
import execjs

session = requests.session()

proxy = {'http': 'http://{}:{}'.format('117.60.39.2', 894)}


def url_encode(data):
    """token解码"""
    if isinstance(data, str):
        data = data.replace(" ", "").encode()
        base_data = zlib.compress(data)
        data = base64.b64encode(base_data)
        return data
    else:
        data = str(data)
        return url_encode(data)


def test():
    headers = {}
    data = {
        "login": 'hzmszp888',
        "part_key": "",
        "password": 'yangzong665',
        "error": "",
        "success": "",
        "isFetching": 'false',
        "loginType": "account",
        "verifyRequestCode": "",
        "verifyResponseCode": "",
        "captchaCode": "",
        "verifyType": 'null',
        "rohrToken": "dcacacacacac"
        # "rohrToken": requests.get("https://api.chachadian.cn:8201/spiderMsg/getMsg").json()['data']
    }

    res1 = session.post(
        'https://epassport.meituan.com/api/account/login?service=waimai&bg_source=3&loginContinue=http:%2F%2Fe.waimai.meituan.com%2Fv2%2Fepassport%2Fentry&loginType=account',
        data=data,
        headers=headers
    ).json()

    print('res1: ', res1)

    if res1['status']['message'] == '需要滑块验证':
        verifyRequestCode = res1['verifyTO']['verifyRequestCode']

        res2 = session.post('https://verify.meituan.com/v2/ext_api/page_data', data={
            'requestCode': verifyRequestCode,
            'feVersion': '1.4.0',
            'source': '1'
        }).json()
        print('res2: ', res2['data'])

        print('sign', res2['data']['sign'])
        print('session', res2['data']['session'])

        print('json_data: ', json.loads(json.dumps(res2['data']).replace('null', '"null"').replace('false', '"false"')))

        bt_res = requests.post('http://api.qinjiahu.cn/token',
                               data=json.loads(json.dumps(res2['data']).replace('None', '"null"').replace('false', '"false"'))
                               ).json()

        print('bt_res: ', bt_res)

        request_code = res2['data']['request_code']
        print('request_code: ', request_code)

        request_code = input('请输入request_code：')

        headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Content-Length': '1695',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Host': 'verify.meituan.com',
            'Origin': 'https://verify.meituan.com',
        }

        print('token_btoa: ', bt_res['token_btoa'])
        print('behavior: ', bt_res['behavior'])

        res3 = session.post('https://verify.meituan.com/v2/ext_api/merchantlogin/verify?id=71', data={
            'request_code': request_code,
            'fingerprint': 'undefined',
            'behavior': f"{bt_res['behavior']}",
            '_token': f"{bt_res['token_btoa']}"
        }, headers=headers).json()

        print('res3: ', res3)


def test1():
    headers = {
        'Host': 'verify.meituan.com',
        'Origin': 'https://verify.meituan.com',
    }

    res3 = requests.post('https://verify.meituan.com/v2/ext_api/merchantlogin/verify?id=71', data={
        'request_code': '1205561426114f65aa4f86aa99aefad2',
        'fingerprint': 'undefined',
        'behavior': "QPFo/EaRDj7YeGn5cv8B+zCujJbmy7RpWbBCDRN3bA6LU/yCbzv5CjXsXG2ekeXsSf2Qkbj3Am6pRw4rs8OMDUTrMaJK6Y+yztvMOJHjnL9+3VkvFbzYzpV8PWVumQxcSmGASXX1Wz/Uev0L2E40U9SOH6yTa5yD3miP2d586SIW8QqZO19bj/fES9SvdFkQUwN3h1Smz0Kc+yVFeTqqd/0aYRFquVd0u1+wTueR/GPYbKhyigIMy/tml2cDRqQ6V5WxlbvqKAt8C6+7D0S9YJ2eHUl904/W",
        # 'behavior': "qnvcju0lbZepEFGn5XPzjSur06i8GrtAUKA4Bw+PBAIKBLmjkAJLkxz5H9xIQTSkJ6+semLNKNEQMDj3GuLoTWEtzzTTbuWmxbsfErfO7l3VCIi0Gp5cbkgfaX4fNCoqcGNYxOZwlEKQbeSHu/VFIVHE77Tm4r8YrrkqzI+FYKsKnQvkNJ2S4rHr/tN+0bEGP7ylPduhvGQZ46pDAamqbDAGRwLRkL4h+FLhVYPloTzLOn0YvUE3vYzdsLNM0ibusxWGCgYh2WJ4nyAJ2RJ9ta2hHHiC3QCaKASRZJJaw6lkcTlH1h3sALCvj71JMKhz9rBHpSlF1+SDUDxHsnZO2sxyIFKwYQOFsers7K2kT5l1bLqh",
        '_token': "ZUp4dFU5bHVxMGdVL0pVSWFaNndBdDFOUTNlays0RDNtTVhMeFJ0WDg0QXhzYmsyaTFtOGpVYWFyNWtQbXkrWlBpUzVTVVlqV1pncUY5VlY1NWcvcEhOVVNFOFNlbFFmZGFrbEZjOWJRS3FxSWk1Z1ZVcFBpR3FVWVlLSXdWVGVrc0t2SE9lb0pXMktSVmQ2K29FNFZsdElaZXJ2UU0wRTg1bjZnUmhsYi9kWUV4OVFQUXVSdEsrcXZIeFNsQ2dQeWpMUGl1b3hpZUtxRHRMSE1FdVVJQXl6T3EyVU9vMnIrQndkczEyYy92UFgzOUhqSllpVElQNnMvUTMzejFoY2ZobUorM0FmcEx0b2N0bUtPbkFRblBNL2p5ckNOMHVWcUNpeVFoSDlrU1RpSlI3RU16VGNlc0JVYlQxd1E1Z1lsQWlvaXd0bkFpSkVxTUFNQ1F3alkxb0Q5ZGFEY0dsKzUvcWJIcWt3WW9ZNFlBUVkvQ2czQkRZdzRFK0djQjVTd1pHekJqT0JFVGhTdFFsZ0FFWk5JT05kajdEQUdoeU9xUWFZd0lGaUJXOEJrQ2F3VGhoZzBHUFE4eWF4UVFHREhtRWRETFNHMEY0clFHVGVFTFFoTkFRbElRTFdQeEZRQWtNcHBHSVltZ0VoTUxTaUJvU2d6Uk84YWQyVWdpa1FLTVVNTURBZ0pFR05JOEx2WXlHNGFZM2ZwMEJJWXdCVFlCd3doT1FOMWhyOG1oRTFrU0EwMFdHYkI5aW0rQTZhclNLa053Y0lrZmtxRVI0RUhvSDlmbEN2MnhNOWhwNWp2N092SzREMDdibm5qZDBQQS9ZMnVWOEdxTmtNMXRsL3RVeFQzOWI0bFJmL2ttWWY0b0ZuZHpMM1BvejBwcUh4aFJkOXF2ZGVqbmgxaFRCTzh4cGVVdUEyZFZWbDZUc29zb24wOUJJY3k2Z2xsZkV1RmZwb2RISHZoOW9JRDZacGpydEt1UGNydTczemorcmNSc3didWY0Y2svdDRQWjNGVnR4WGxEUmFHaEZodDVVMW9FWWxEeSszSHJ0bWJWb1B6N1ptSDczOTZScU4rNFZlZTNWeVdTejBqWGU3cEh3UVJvVnVXK055YlFRclI5TjNxaFh2YjBNcjVMZnVZTHRPdFhKRC9aVThKVDQ3blg2R2gyaXk2NGRIeDBoVzIzdnA1YlF6cmZHOUhzMEtmWG91cjh0azFybnFmdVFraHMzMVd4ZE5hMFBiOUt3cTYvcnlyRDdZMTUxSXFkRDBWRHJxMGw4azdKYnRUYmx2RGUwaExnZmpreklONXV0UnBTYWJvWnpqbWhkSGtyY2RML1RwZHV6MmJzczZ1TXhTTFZ3T3FmK3lzbzQwN1phNXVpSlROd2k5a1dMT2crVXhXaHVtaFViTGV4VDVRWGpHZ1d5bXhCbTFEZFdWWTU5bituM2ZueDNSTEpWNWIrSFM0dURPMTBsN1UvaWJYcnJJS1RsZHZZeFJuZVBEaHQyNHJsb3plMHVMa1pzSDN1QTRZS2JYa2RQWmM1SzY3V202bXZZV3QzSFhMSmk3NitQSlQ5TGZENnFUbmJGek5lMThYMjV1OS9tZWpyMXdtWFhKcnQwZnB6VXAwbkE3WHVxQlV4YTM3dzRmbURiZTFtVzNyWmdLUG5scnphMlc4MFZhRDFkS1ljV2x2TC9Rc2xSVlVpSTh2d1JPUDd4M1ZzRWhqeGR5VjVZREx3c245a3ZuSmR3TWlsaHpldHRFWVhMZHZzcjVDMmw3K25QYk1qa1pPdGJNTUUxbnpROUo3MkQxOHQ3dStUSzZLbWZuWmFCYVdzZjg5azM2ODE5WFE3U3g="
    }, headers=headers).json()

    print(res3)


if __name__ == '__main__':
    test()
    # test1()

    # a = {'riskLevel': '71', 'succCallbackUrl': None, 'theme': None, 'request_code': '12377e83c0da46fa9a02ff44164a8b98', 'yodaVersion': '{"i":"5747080725c2801e","d":"ed789690d8b8d5d4"}', 'isJumpToI': None, 'type': '71', 'country': '中国大陆', 'mobileInterCode': '86', 'sign': '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', 'category': 'SINGLE', 'defaultIndex': 0, 'verifyMethodVersion': '{"slider":"{\\"i\\":\\"ab08e567557d68aa\\",\\"d\\":\\"99fa8f96b6488d17\\"}"}', 'needInput': None, 'session': 'cmV0dXJuIGZ1bmN0aW9uKHgseSx6KXtyZXR1cm4gbmV3IHgobmV3IHooWzEwNCwgOSwgOTQsIC0yNCwgLTk3LCAtMTEzLCAzMywgNTQsIDM5LCAtMTA4LCAxMjcsIDksIC0xMDIsIC03NywgLTgwLCAtNjhdKSx5KTt9', 'riskLevelInfo': '{"71":"{\\"desc\\":\\"滑块\\",\\"name\\":\\"slider\\"}"}', 'encType': 2, 'isDegrade': False, 'action': 'merchantlogin', 'autoSend': None, 'notifyUrl': None, 'failCallbackUrl': None}
    #
    # b = json.dumps(a)
    # print('b: ', b)
    # c = b.replace('null', '"null"').replace('false', '"false"')
    # print('c: ', c)
    # d = json.loads(c)
    # print('d: ', d)


