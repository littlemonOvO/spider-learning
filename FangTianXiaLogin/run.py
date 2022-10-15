# _*_ coding: utf-8 _*_
# @Time: 2022/10/15 11:41
# @Author: lemon
# @File: run
# @Project: spider-100
import pprint

import execjs
import requests

from common.utils import get_common_headers


def pwd_encrypt(password):
    with open('./exec.js', 'r') as f:
        js = f.read()
    js_compiler = execjs.compile(js)
    pwd_encrypted = js_compiler.call('pwdEncrypted', password)
    return pwd_encrypted


# 房天下加密接口逆向 -rsa加密
def run():
    headers = {
        'referer': 'https://passport.fang.com/'
    }
    headers.update(get_common_headers())
    url = 'https://passport.fang.com/login.api'
    username = 'abc'
    password = '123456'
    pwd_encrypted = pwd_encrypt(password)
    params = {
        'uid': username,
        'pwd': pwd_encrypted,
        'Service': 'soufun-passport-web',
        'AutoLogin': 1
    }
    resp = requests.get(url, headers=headers, params=params)
    assert resp.status_code == 200
    pprint.pprint(resp.json())


if __name__ == '__main__':
    run()
