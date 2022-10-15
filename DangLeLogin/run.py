# _*_ coding: utf-8 _*_
# @Time: 2022/10/14 20:19
# @Author: lemon
# @File: run
# @Project: spider-100
import pprint

import execjs
import requests

from common.utils import get_common_headers


def encryptPassword(pwd):
    with open('./exec.js', 'r') as f:
        js = f.read()
    js_compiler = execjs.compile(js)
    pwd_encrypt = js_compiler.call('rsaEncrypted', pwd)
    return pwd_encrypt


def run():
    url = 'https://oauth.d.cn/auth/login'
    headers = {
        'referer': 'https://oauth.d.cn/auth/goLogin.html',
    }
    headers.update(get_common_headers())
    # 用户密码
    username = 'user'
    pwd = '123456'
    # 对密码进行rsa加密
    pwd_encrypt = encryptPassword(pwd)
    params = {'display': 'web', 'name': username, 'to': 'https://www.d.cn/', 'pwd': pwd_encrypt}
    resp = requests.get(url, params=params, headers=headers)
    assert resp.status_code == 200
    pprint.pprint(resp.json())


if __name__ == '__main__':
    run()
