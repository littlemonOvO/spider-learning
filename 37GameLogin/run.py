# _*_ coding: utf-8 _*_
# @Time: 2022/10/15 15:00
# @Author: lemon
# @File: run
# @Project: spider-100
import random
import time

import execjs
import requests

from common.utils import get_common_headers


def encrypt_password(password):
    with open('./exec.js', 'r', encoding='utf-8') as f:
        js = f.read()
    js_compiler = execjs.compile(js)
    pwd = js_compiler.call('encrypt', password)
    return pwd


# 37网游登录接口 -rsa加密
def run():
    url = 'https://my.37.com/api/login.php'
    headers = {
        'referer': 'https://www.37.com/'
    }
    headers.update(get_common_headers())
    username = 'abcbc'
    password = '123456'
    timestamp = str(int(time.time() * 1000))
    jsonp = ''
    for _ in range(20):
        jsonp += str(random.randint(0, 9))
    callback = 'jQuery' + jsonp + '_' + timestamp
    params = {
        "callback": callback,
        "action": "login",
        "login_account": username,
        "password": encrypt_password(password),
        "ajax": 0,
        "remember_me": 1,
        "save_state": 1,
        "ltype": 1,
        "tj_from": 100,
        "s": 1,
        "tj_way": 1,
        "_": timestamp
    }
    resp = requests.get(url, params=params, headers=headers)
    assert resp.status_code == 200
    print(resp.text)


if __name__ == '__main__':
    run()
