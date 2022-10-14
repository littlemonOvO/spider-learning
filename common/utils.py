# _*_ coding: utf-8 _*_
# @Time: 2022/9/13 16:44
# @Author: lemon
# @File: utils
# @Project: spider-100

import base64

from Crypto.Cipher import AES
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


"""
AES加密所需参数:
    |   参数   |         作用及数据类型        |
    |   密钥   |  加解密时使用,数据类型为bytes  |    
    |   明文   | 需要加密的参数,数据类型为bytes |
    |   模式   |       ECB和CBC为常用模式      |
    | iv偏移量 |  CBC模式下需要,数据类型为bytes |
"""


class AESCryptor:
    def __init__(self, secret_key, mode, iv=''):
        self.secret_key = secret_key
        self.iv = iv
        if mode == AES.MODE_CBC:
            self.aes = AES.new(self.add_to_16(self.secret_key), mode, self.add_to_16(iv))
        elif mode == AES.MODE_ECB:
            self.aes = AES.new(self.add_to_16(self.secret_key), mode)

    # 将str位数补足到16的倍数
    @staticmethod
    def add_to_16(value):
        while len(value) % 16 != 0:
            value += '\0'
        return str.encode(value)

    # 加密
    def aes_encrypt(self, text):
        encrypt_aes = self.aes.encrypt(self.add_to_16(text))
        encrypted_text = str(base64.encodebytes(encrypt_aes), encoding='utf-8')
        return encrypted_text

    # 解密
    def aes_decrypt(self, text):
        base64_decrypted = base64.decodebytes(text.encode(encoding='utf-8'))
        decrypted_text = str(self.aes.decrypt(base64_decrypted), encoding='utf-8').replace('\0', '')
        return decrypted_text
