import json
import requests


url = 'http://api.map.baidu.com/geocoder'
output = 'json'
ak = 'f247cdb592eb43ebac6ccd27f796e2d2'

a = ['北京', '天津', '石家庄', '太原', '呼和浩特', '沈阳', '大连', '长春', '哈尔滨', '上海', '南京', '杭州', '宁波', '合肥', '福州', '厦门', '南昌', '济南',
     '青岛', '郑州', '武汉', '长沙', '广州', '深圳', '南宁', '海口', '重庆', '成都', '贵阳', '昆明', '拉萨', '西安', '兰州', '西宁', '银川', '乌鲁木齐']


for i in a:
    add = quote(i)
    uri = url + '?' + 'address=' + add + '&output=' + output + '&ak=' + ak  # 百度地理编码API
    req = urlopen(uri)
    res = req.read().decode()
    temp = json.loads(res)

    print(temp['result']['location']['lng'], temp['result']['location']['lat'])  # 打印出经纬度

