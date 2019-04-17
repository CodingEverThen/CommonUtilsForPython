#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    @Time    : 2019/4/12
    @Author  : LXW
    @Site    : 
    @File    : FileDecryptEncrypt.py
    @Software: PyCharm
    @Description: 
"""
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
import base64
import traceback
import os

import utils.LoggerUtil as loggerUtil


class FileDecryptEncrypt():
    def __init__(self):
        try:
            self.private_key = RSA.import_key(open(os.path.join(os.path.dirname(os.getcwd()), "config", "rsa_private_key.pem")).read())
            self.rsa_public_key = RSA.import_key(open(os.path.join(os.path.dirname(os.getcwd()), "config", "rsa_public_key.pem")).read())
        except Exception as e:
            traceback.print_exc()
            loggerUtil.error("加载密钥出现异常")

    def decryptAES(self, root_path, res_path):
        try:
            file_in = open(root_path, "rb")
            enc_session_key, nonce, tag, ciphertext = \
                [file_in.read(x) for x in (self.private_key.size_in_bytes(), 16, 16, -1)]
            # Decrypt the session key with the private RSA key
            cipher_rsa = PKCS1_OAEP.new(self.private_key, hashAlgo=SHA256)
            session_key = cipher_rsa.decrypt(enc_session_key)
            # Decrypt the data with the AES session key
            cipher_aes = AES.new(session_key, AES.MODE_EAX, nonce)
            data = cipher_aes.decrypt_and_verify(ciphertext, tag)
            # 返回解密后的数据
            with open(res_path, "w+") as resf:
                print(data.decode("utf-8"))
                resf.write(data.decode("utf-8"))
            return True
        except Exception as e:
            traceback.print_exc()
        return False

    def decrypt(self, root_path, res_path):
        """
        RSA的文件解密
        :param root_path: 加密后的文件
        :param res_path: 解密后的文件
        :return: 解密结果
        """
        new_line = b""
        cipher = PKCS1_OAEP.new(self.private_key, hashAlgo=SHA256)
        try:
            with open(root_path, "r") as rootf:
                lines = rootf.read().split("==")
            for line in lines:
                if len(line) > 0:
                    line = line + "=="
                    b64_decoded_message = base64.b64decode(line)
                    cipherContent = cipher.decrypt(b64_decoded_message)
                    new_line = new_line + cipherContent
            if not os.path.exists(os.path.dirname(res_path)):
                os.makedirs(os.path.dirname(res_path))
            with open(res_path, "w") as resf:
                resf.write(str(new_line, encoding="UTF-8").replace("\r\n", "\n"))
            return True
        except Exception as e:
            traceback.print_exc()
        return False

    def encrypt(self, root_path, res_path):
        try:
            # 数据源
            data = open(root_path).read().encode("utf-8")
            # 输出源
            file_out = open(res_path, "wb")
            session_key = get_random_bytes(16)
            # Encrypt the session key with the public RSA key
            cipher_rsa = PKCS1_OAEP.new(self.rsa_public_key)
            enc_session_key = cipher_rsa.encrypt(session_key)
            # Encrypt the data with the AES session key
            cipher_aes = AES.new(session_key, AES.MODE_EAX)
            ciphertext, tag = cipher_aes.encrypt_and_digest(data)
            [file_out.write(x) for x in (enc_session_key, cipher_aes.nonce, tag, ciphertext)]
            return True
        except Exception as e:
            traceback.print_exc()
        return False

# if __name__ == '__main__':
#     FileDecryptEncrypt().decrypt("F:\\868663032830438_migu$user$login$_1554947856915.log","C:\\Users\\Carol\\Desktop\\others\\868663032830438_migu$user$login$_1554947856915.log")