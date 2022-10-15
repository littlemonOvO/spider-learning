# _*_ coding: utf-8 _*_
# @Time: 2022/10/14 10:05
# @Author: lemon
# @File: run
# @Project: spider-100
import json
import pprint
from binascii import a2b_hex

import execjs
import requests
from Crypto.Cipher import AES

from common.utils import get_common_headers


def get_data_by_js(text):
    with open('./exec.js', 'r', encoding='utf-8') as f:
        js = f.read()
    js_compiler = execjs.compile(js)
    result = js_compiler.call('getDecryptedData', text)
    return result


# AES解密python实现
def get_data_by_python(text):
    key = 'jo8j9wGw%6HbxfFn'.encode('utf-8')
    iv = '0123456789ABCDEF'.encode('utf-8')
    aes = AES.new(key=key, mode=AES.MODE_CBC, iv=iv)
    # hexstr解码
    srcs = a2b_hex(text.encode('utf-8'))
    decrypt_text = aes.decrypt(srcs).strip(''.encode()).decode()
    return decrypt_text


def run():
    headers = {
        'referer': 'https://jzsc.mohurd.gov.cn/data/company'
    }
    headers.update(get_common_headers())
    url = 'https://jzsc.mohurd.gov.cn/api/webApi/dataservice/query/comp/list?pg=1&pgsz=15&total=450'
    resp = requests.get(url, headers=headers)
    assert resp.status_code == 200
    # AES加密
    # result = get_data_by_js(resp.text)
    result = get_data_by_python(resp.text)
    pprint.pprint(json.loads(result))


if __name__ == '__main__':
    run()
