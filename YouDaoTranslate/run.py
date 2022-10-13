# _*_ coding: utf-8 _*_
# @Time: 2022/10/12 15:56
# @Author: lemon
# @File: run
# @Project: spider-100
import hashlib
import pprint
import random
import time

import execjs
import requests

from common.utils import get_common_headers


# 通过js获取加密参数
def get_param_by_js(query, ua):
    js = open('./exec.js', 'r').read()
    js_compiler = execjs.compile(js)

    result = js_compiler.call('func', query, ua)
    return {
        'salt': result['salt'],
        'sign': result['sign'],
        'lts': result['ts'],
        'bv': result['bv']
    }


# 通过python获取加密参数
def get_param_by_python(query, ua):
    bv = hashlib.md5(ua.encode()).hexdigest()
    ts = int(time.time() * 1000)
    salt = random.randint(0, 10) + ts
    sign = hashlib.md5(str('fanyideskweb' + query + str(salt) + 'Ygy_4c=r#e#4EX^NUGUc5').encode()).hexdigest()
    return {
        'bv': bv,
        'lts': ts,
        'salt': salt,
        'sign': sign
    }


def run(query):
    headers = get_common_headers()
    headers.update({
        # 必需字段
        "Referer": "https://fanyi.youdao.com/",
    })
    cookies = {
        "OUTFOX_SEARCH_USER_ID": "1672645646@10.108.162.135",
        "OUTFOX_SEARCH_USER_ID_NCOO": "992989395.0026644",
        # "___rl__test__cookies": "1665563315630"
    }
    url = "https://fanyi.youdao.com/translate_o"
    params = {
        "smartresult": "rule"
    }
    data = {
        "i": "webs",
        "from": "AUTO",
        "to": "AUTO",
        "smartresult": "dict",
        "client": "fanyideskweb",
        # 加密参数
        "salt": "",
        "sign": "",
        "lts": "",
        "bv": "476414572dc9132c2e6562015cc36254",
        "doctype": "json",
        "version": "2.1",
        "keyfrom": "fanyi.web",
        "action": "FY_BY_REALTlME"
    }

    # js获取加密参数
    # result = get_param_by_js(query, headers['User-Agent'])
    result = get_param_by_python(query, headers['User-Agent'])
    # 可选
    # cookies['___rl__test__cookies'] = str(int(time.time() * 1000))

    data['i'] = query
    data.update(result)
    pprint.pprint(data)

    response = requests.post(url, headers=headers, cookies=cookies, params=params, data=data)
    print(response.text)


if __name__ == '__main__':
    run('translate')
