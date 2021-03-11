import re
import time
import uuid
from datetime import datetime, date
import hashlib

import os

import zlib
import base64

import geoip2.database


def json_serial(obj):
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    # raise TypeError("Type {}s not serializable".format(type(obj)))


def get_md5():
    m1 = hashlib.md5()
    m1.update('{uuid}{time}'.format(time=str(time.time()), uuid=uuid.uuid1()).encode("utf-8"))
    token = m1.hexdigest()
    return token[8: 25]


def str_to_dict(data):
    a = {}
    for i in data.split('&'):
        k_v = i.split('=')
        a[k_v[0]] = k_v[1]
    print(a)


def dict_to_str(data):
    a = ''
    for key, value in data.items():
        a += f'{key}={value}&'
    return a[:-1]


def url_encode(data, rep=True):
    """token编码"""
    if isinstance(data, str):
        if rep:
            data = data.replace(" ", "").encode()
        else:
            data = data.encode()
        base_data = zlib.compress(data)
        data = base64.b64encode(base_data)
        return data


def url_decode(data):
    """token解码"""
    if isinstance(data, str):
        data = base64.b64decode(data)
        base_data = zlib.decompress(data)
        return base_data


def get_ip_data(remote_ip):
    ip = re.findall('^(127\\.0\\.0\\.1)'
                    '|(localhost)|(10\\.\\d{1,3}\\.\\d{1,3}\\.\\d{1,3})'
                    '|(172\\.((1[6-9])|(2\\d)|(3[01]))\\.\\d{1,3}\\.\\d{1,3})'
                    '|(192\\.168\\.\\d{1,3}\\.\\d{1,3})$', remote_ip)

    if ip:
        return False

    else:
        return remote_ip


def get_ip_info(ip):
    ip = get_ip_data(ip)
    if not ip:
        return {}
    reader = geoip2.database.Reader(os.path.join(os.path.dirname(__file__), 'GeoLite2-City.mmdb'))
    response = reader.city(ip)
    return {
        'country': response.country.names["zh-CN"],
        'province':  response.subdivisions.most_specific.names["zh-CN"],
        'city': response.city.names["zh-CN"],
        'lin_lat': f'{response.location.longitude}|{response.location.latitude}'
    }


if __name__ == '__main__':
    get_ip_info('58.101.33.178')
