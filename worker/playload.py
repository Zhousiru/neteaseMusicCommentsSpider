# -*- coding: UTF-8 -*-

from Crypto.Cipher import AES
import base64
import codecs
import os
import json

modulus = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
nonce = '0CoJUm6Qyw8W8jud'
pubKey = '010001'


def aesEncrypt(text, secKey):
    pad = 16 - len(text) % 16
    if isinstance(text, bytes):
        text = text.decode('utf-8')
    text = text + str(pad * chr(pad))
    encryptor = AES.new(secKey, 2, '0102030405060708')
    ciphertext = encryptor.encrypt(text)
    ciphertext = base64.b64encode(ciphertext)

    return ciphertext


def rsaEncrypt(text):
    text = text[::-1]
    rs = int(codecs.encode(text.encode('utf-8'), 'hex_codec'),
             16)**int(pubKey, 16) % int(modulus, 16)

    return format(rs, 'x').zfill(256)


def createSecretKey(size):
    return (''.join(map(lambda xx: (hex(ord(xx))[2:]), str(os.urandom(size)))))[0:16]


def getPlayload(info):
    info = json.dumps(info)
    secKey = createSecretKey(16)
    encText = aesEncrypt(aesEncrypt(info, nonce), secKey)
    encSecKey = rsaEncrypt(secKey)

    return {
        'params': encText,
        'encSecKey': encSecKey
    }
