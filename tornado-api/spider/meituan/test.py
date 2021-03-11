import execjs
#
# null = 'null'
# false = 'false'
#
# node = execjs.get()
#
# ctx = node.compile(open('slider.js', encoding='utf-8').read())
#
# p = ctx.eval('get_behavior_token("{config}")'.format(config={
#     "riskLevel":"71",
#     "succCallbackUrl":null,
#     "theme":null,
#     "request_code":"f07b7756d1d54976987f3f2d2ba05a7a",
#     "yodaVersion":'{"i":"5747080725c2801e","d":"ed789690d8b8d5d4"}',
#     "isJumpToI":null,
#     "type":"71",
#     "country":"中国大陆",
#     "mobileInterCode":"86",
#     "sign":"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",
#     "category":"SINGLE",
#     "defaultIndex":0,
#     "verifyMethodVersion":'{"slider":"{"i":"ab08e567557d68aa","d":"99fa8f96b6488d17"}"}',
#     "needInput":null,
#     "session":"cmV0dXJuIGZ1bmN0aW9uKHgseSx6KXtyZXR1cm4gbmV3IHgobmV3IHooWzI4LCAtOTgsIC0xOCwgLTQzLCAtOTUsIC0zNCwgLTExMywgLTUyLCA3MywgMSwgOTMsIDU5LCAxOCwgLTM1LCAxMCwgNjddKSx5KTt9",
#     "riskLevelInfo":'{"71":"{"desc":"滑块","name":"slider"}"}',
#     "encType":2,
#     "isDegrade":false,
#     "action":"merchantlogin",
#     "autoSend":null,
#     "notifyUrl":null,
#     "failCallbackUrl":null
# }))
#
# print(p)

import requests
import json


null = "null"
false = "false"

# {'riskLevel': '71', 'succCallbackUrl': 'null', 'theme': 'null', 'request_code': 'e4b56fa644e8424ab7fc62679c64a651', 'yodaVersion': '{"i":"5747080725c2801e","d":"ed789690d8b8d5d4"}', 'isJumpToI': 'null', 'type': '71', 'country': '中国大陆', 'mobileInterCode': '86', 'sign': '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', 'category': 'SINGLE', 'defaultIndex': 0, 'verifyMethodVersion': '{"slider":"{\\"i\\":\\"ab08e567557d68aa\\",\\"d\\":\\"99fa8f96b6488d17\\"}"}', 'needInput': 'null', 'session': 'cmV0dXJuIGZ1bmN0aW9uKHgseSx6KXtyZXR1cm4gbmV3IHgobmV3IHooWy01NCwgLTExNiwgNDMsIC0xMCwgLTgxLCAtOTAsIC0xMjAsIC04MCwgLTc3LCAyNSwgLTU1LCAtNTQsIC0zNSwgNTEsIC0xOCwgLTg2XSkseSk7fQ==', 'riskLevelInfo': '{"71":"{\\"desc\\":\\"滑块\\",\\"name\\":\\"slider\\"}"}', 'encType': 2, 'isDegrade': 'false', 'action': 'merchantlogin', 'autoSend': 'null', 'notifyUrl': 'null', 'failCallbackUrl': 'null'}

url = 'http://api.qinjiahu.cn/set_code?code=929777'
# url = 'http://api.qinjiahu.cn/get_code'

res = requests.get(url)
# res.encoding = 'gb2312'

print(res.text)
