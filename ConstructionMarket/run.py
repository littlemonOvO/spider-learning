# _*_ coding: utf-8 _*_
# @Time: 2022/10/14 10:05
# @Author: lemon
# @File: run
# @Project: spider-100
import json
import pprint

import execjs
import requests

from common.utils import get_common_headers


def get_data_by_js(text):
    with open('./exec.js', 'r', encoding='utf-8') as f:
        js = f.read()
    js_compiler = execjs.compile(js)
    result = js_compiler.call('getDecryptedData', text)
    pprint.pprint(json.loads(result))


def run():
    headers = {
        'referer': 'https://jzsc.mohurd.gov.cn/data/company'
    }
    headers.update(get_common_headers())
    url = 'https://jzsc.mohurd.gov.cn/api/webApi/dataservice/query/comp/list?pg=1&pgsz=15&total=450'
    resp = requests.get(url, headers=headers)
    assert resp.status_code == 200
    # AES加密
    get_data_by_js(resp.text)


if __name__ == '__main__':
    run()
