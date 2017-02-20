# -*- coding: utf-8 -*-

import abc

import os

from Crypto import Random
from Crypto.Cipher import AES
import base64
import hashlib


class User(object):
    email = None
    fullName = None
    username = None
    encPassword = None

    def __init__(self):
        pass


class SessionManager(object):
    users = None
    db = None

    def __init__(self):
        self.db = "../../data/users.data"
        lines = [line.strip() for line in file(self.db)]
        self.users = {}
        for line in lines:
            pieces = line.split(',')

            user = {}
            user["username"] = pieces[0]
            user["password"] = pieces[1]
            user["Name"] = pieces[2]

            self.users[user["username"]] = user

    def validateCredentials(self, username, plainPassword):

        if username in list(self.users.keys()):
            encDBPass = self.users[username]["password"]
            encPass = AESCryptoManager.getHash(plainPassword)

            if encDBPass == encPass:
                return True

        return False


class CryptoManager(object, metaclass=abc.ABCMeta):
    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s) - 1:])]

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    @abc.abstractmethod
    def encrypt(self, plainText):
        pass

    @abc.abstractmethod
    def decrypt(self, encryptedText):
        pass


class AESCryptoManager(CryptoManager):
    key = None
    bs = None

    def __init__(self, key):
        self.bs = 32
        self.key = self.getHash(key)

    def encrypt(self, raw):
        raw = self._pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw))

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')

    @staticmethod
    def getHash(text):
        return hashlib.sha256(text.encode()).hexdigest()


if __name__ == '__main__':
    """
    text = "mcollado"
    enc = AESCryptoManager.getHash(text)
    print enc
    """

    sm = SessionManager()
    print(sm.validateCredentials("asanso", "asanso"))
