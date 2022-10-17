# _*_ coding: utf-8 _*_
# @Time: 2022/10/17 9:41
# @Author: lemon
# @File: run
# @Project: spider-100
import hashlib
import urllib.parse

import requests

from common.utils import get_common_headers

"""
    新接口中对user参数进行了加密，不再是以前的明文传输，但实测目前明文传输user仍然有效
    user使用了随机密钥的AES加密，并对生成的随机密钥进行了进一步(rsa？)加密，
    并附在登录接口的请求头中的EUI字段中传输，暂未能破解其加密方式。
"""


def encrypt_user(username):
    pass


# 从重定向的headers中取得部分接口参数
def get_param(headers):
    url = 'https://account.xiaomi.com/'
    resp = requests.get(url, headers=headers)
    location_url = resp.history[1].headers['Location']
    urlparse = urllib.parse.urlparse(location_url)
    query_dict = urllib.parse.parse_qs(urlparse.query)
    return {
        'showActiveX': query_dict['showActiveX'][0],
        'serviceParam': query_dict['serviceParam'][0],
        'callback': query_dict['callback'][0],
        'qs': query_dict['qs'][0],
        'sid': query_dict['sid'][0],
        '_sign': query_dict['_sign'][0],
        'needTheme': query_dict['needTheme'][0]
    }


def run(username, password):
    url = 'https://account.xiaomi.com/pass/serviceLoginAuth2'
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Pragma": "no-cache",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "sec-ch-ua": "\"Chromium\";v=\"106\", \"Microsoft Edge\";v=\"106\", \"Not;A=Brand\";v=\"99\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\""
    }
    headers.update(get_common_headers())
    data = get_param(headers)

    data.update({
        # user字段待加密
        'user': username,
        'hash': hashlib.md5(password.encode()).hexdigest().upper(),
        'policyName': 'miaccount',
        'bizDeviceType': '',
        'theme': '',
        'cc': '+86',
        '_json': True,
        'captCode': ''
    })

    resp = requests.post(url, headers=headers, data=data)
    assert resp.status_code == 200
    print(resp.text)


if __name__ == '__main__':
    run('username', 'password')
