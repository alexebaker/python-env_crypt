from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import

import os
import dotenv
import base64
import hashlib
import subprocess

from Crypto.Cipher import AES
from Crypto import Random


def load_env(env_path, password='', keyfile=''):
    dotenv.load_dotenv(env_path)

    enc_key = get_key(password, keyfile)
    values = dotenv.main.dotenv_values(env_path)
    for key in values.keys():
        if key != 'salt':
            enc_value = os.environ[key]
            dec_value = decrypt_string(enc_value, enc_key)
            os.environ[key] = dec_value
    return


def update_env(env_path, key='', value='', password='', keyfile=''):
    if key is None or value is None:
        raise ValueError("You must specify a key and a value"
                         " to update the env file.")

    enc_key = get_key(password, keyfile)
    enc_value = encrypt_string(value, enc_key)
    dotenv.set_key(env_path, key, enc_value)
    return


def list_env(env_path, password='', keyfile=''):
    enc_key = get_key(password, keyfile)
    values = dotenv.main.dotenv_values(env_path)
    for key, value in values.items():
        if key != 'salt':
            dec_value = decrypt_string(value, enc_key)
        else:
            dec_value = value
        print('%s="%s"' % (key, dec_value))
    return


def encrypt_env(env_path, password='', keyfile=''):
    enc_key, salt = get_key(password, keyfile)
    dotenv.set_key(env_path, 'salt', salt)

    values = dotenv.main.dotenv_values(env_path)
    for key, value in values.items():
        if key != 'salt':
            enc_value = encrypt_string(value, enc_key)
            dotenv.set_key(env_path, key, enc_value)
    return


def decrypt_env(env_path, password='', keyfile=''):
    salt = dotenv.get_key(env_path, 'salt')
    enc_key = get_key(password, keyfile, salt=salt)

    values = dotenv.main.dotenv_values(env_path)
    for key, value in values.items():
        if key != 'salt':
            dec_value = decrypt_string(value, enc_key)
            dotenv.set_key(env_path, key, dec_value)
    return


def get_key(password, keyfile, salt=None):
    if password is not None:
        key = password
    elif keyfile is not None:
        with open(keyfile, 'r') as f:
            key = f.read()
    else:
        raise ValueError("You must specify either a password or keyfile.")

    if key > 1024:
        key = key[:1024]

    if salt is None:
        salt = Random.new().read(256)

    enc_key = hashlib.pbkdf2_hmac('sha256', key, salt, 100000)
    return enc_key, salt


def encrypt_string(plaintext, key):
    iv = Random.new().read(AES.block_size)
    aes = AES.new(key, AES.MODE_CFB, iv)

    ciphertext = base64.b64encode(iv + aes.encrypt(plaintext))
    return ciphertext


def decrypt_string(ciphertext, key):
    ciphertext = base64.b64decode(ciphertext)
    iv = ciphertext[:AES.block_size]
    aes = AES.new(key, AES.MODE_CFB, iv)

    plaintext = aes.decrypt(ciphertext[AES.block_size:])
    return plaintext
