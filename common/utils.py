# _*_ coding: utf-8 _*_
# @Time: 2022/9/13 16:44
# @Author: lemon
# @File: utils
# @Project: spider-100

from fake_useragent import UserAgent

ua = UserAgent(path='../common/static/fake_useragent.json')


def get_common_headers():
    headers = {
        'User-Agent': get_chrome_ua()
    }
    return headers


def get_chrome_ua():
    return ua.Chrome


def get_random_ua():
    return ua.random


class NetworkException(RuntimeError):
    def __init__(self, code, msg):
        self.code = code
        self.msg = msg

    def __str__(self):
        print(f'code:{self.code}, message:{self.msg}')
