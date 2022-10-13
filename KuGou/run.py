# _*_ coding: utf-8 _*_
# @Time: 2022/9/16 11:19
# @Author: lemon
# @File: run
# @Project: spider-100
import json
import pprint
import re
import time

import execjs
import requests

from common.utils import get_common_headers


def getParams(keyword):
    # 构建options参数
    params = {}
    # cookie
    cookie = r'kg_mid=740ce5f255eb190bb2b3c00510cef1d9; ' \
             r'kg_dfid=08xssi1fpHTG0Iye0N1HoPsl; ' \
             r'kg_dfid_collect=d41d8cd98f00b204e9800998ecf8427e; ' \
             r'kg_mid_temp=740ce5f255eb190bb2b3c00510cef1d9; ' \
             r'Hm_lvt_aedee6983d4cfc62f509129360d6bb3d=1663298052,1663308160; ' \
             r'Hm_lpvt_aedee6983d4cfc62f509129360d6bb3d=1663308160'
    # default参数
    defaults = {
        'page': 1,
        'pagesize': 30,
        'bitrate': 0,
        'isfuzzy': 0,
        'inputtype': 0,
        'platform': "WebFilter",
        'clientver': 1e3,
        'iscorrection': 1,
        'privilege_filter': 0,
        'callback': "callback123",
        'filter': 10,
        'keyword': keyword,
    }
    params.update(defaults)
    params['appid'] = 1014
    params['mid'] = '740ce5f255eb190bb2b3c00510cef1d9'
    params['dfid'] = '08xssi1fpHTG0Iye0N1HoPsl'
    params['userid'] = '0'
    params['token'] = ''
    params['uuid'] = params['mid']
    params['clienttime'] = int(time.time())
    params['srcappid'] = '2919'

    s = []
    keys = list(params.keys())
    keys.sort()
    for key in keys:
        s.append(f'{key}={params[key]}')
    s.insert(0, 'NVPh5oo715z5DIWAeQlhMDsWXXQV4hwt')
    s.append('NVPh5oo715z5DIWAeQlhMDsWXXQV4hwt')
    # 调用js生成签名
    js_code = open('./exec.js', encoding='utf-8').read()
    js = execjs.compile(js_code)
    signature = js.call('get', ''.join(s))
    params['signature'] = signature
    return params


def search(keyword):
    headers = get_common_headers()
    pprint.pprint(headers)
    url = 'https://complexsearchretry.kugou.com/v2/search/song'
    params = getParams(keyword)
    resp = requests.get(url, headers=headers, params=params).text
    json_data = json.loads(re.search(r'callback123\((.*)\)', resp).group(1))
    return json_data


def run():
    pprint.pprint(search('曹操'))


def test():
    search('曹操')


if __name__ == '__main__':
    run()
