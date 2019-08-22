# -*- coding: utf-8 -*-
"""
Time    : 2019-08-20 17:52
Author  : Yaodi
Object  : 
"""

import base64
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5


def crack_pwd(pwd, pub_key):
    key = base64.b64decode(pub_key.encode()).decode()
    rsakey = RSA.importKey(key)
    cipher = Cipher_pkcs1_v1_5.new(rsakey)  # 生成对象
    cipher_text = base64.b64encode(cipher.encrypt(pwd.encode(encoding="utf-8")))  # 对传递进来的用户名或密码字符串加密
    value = cipher_text.decode('utf8')  # 将加密获取到的bytes类型密文解码成str类型
    return value
