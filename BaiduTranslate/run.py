# _*_ coding: utf-8 _*_
# @Time: 2022/10/11 9:31
# @Author: lemon
# @File: run
# @Project: spider-100
import pprint
import re

import execjs
import requests

from common.utils import get_common_headers


# js逆向解析sign参数
def get_sign(query, gtk):
    js = open('./func.js', 'r').read()
    js_compiler = execjs.compile(js)
    sign = js_compiler.call('func', query, gtk)
    return sign


def run(query):
    headers = {
        # Acs-Token参数暂未找到破解方法，先使用固定值
        'Acs-Token': '1665385530031_1665453986436_XknKPzsi1EwtBy9FUibxBCo3YwouR1SoeVXAr+iuhwe11YIQliLa90qV12GPVRoT4uRad2naWuzu2tSP4ojH3vfYvXmfQ7z17GR4GCoTTpfEaIuxVB/2vIfSCFy05eHzc23FUn6Vp+MKNREgvG5w6ltxMvMLIrx8QyVEeqbUWVBVmJXeKTuwTXnXcUhOHZRJObqn8abn4KKs54p61bltVlZMcxweoPqxBAFfoExC3+HnoClTMLuVhOuG2dRvvUtiANKUxpIWhKJYjoN0PkzhmlQXD1ApzZkVC0h5+V4mf0LiMBTXWX5uCjetml4HGlZfT1UlPLpz5/t1tj+nJhHphw=='
    }
    headers.update(get_common_headers())
    url = 'https://fanyi.baidu.com/'
    session = requests.session()
    resp = session.get(url, headers=headers)
    assert resp.status_code == 200
    token = re.search("token: '(.*?)'", resp.text).group(1)
    gtk = re.search('window.gtk = "(.*?)"', resp.text).group(1)

    param = {
        'from': 'zh',
        'to': 'en',
        'query': query,
        'simple_means_flag': 3,
        'sign': get_sign(query, gtk),
        'token': token,
        'domain': 'common'
    }

    url = 'https://fanyi.baidu.com/v2transapi?from=en&to=zh'
    resp = session.post(url, data=param, headers=headers)
    assert resp.status_code == 200
    pprint.pprint(resp.json())


if __name__ == '__main__':
    run('translate')
