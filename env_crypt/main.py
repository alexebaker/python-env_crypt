from __future__ import unicode_literals
from __future__ import print_function

import os
import dotenv
import base64
import hashlib

from Crypto.Cipher import AES
from Crypto import Random


def load_env(env_path, password='', keyfile=''):
    dotenv.load_dotenv(env_path)

    enc_key = get_key(password, keyfile)
    values = dotenv.main.dotenv_values(env_path)
    for key in values.keys():
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
        dec_value = decrypt_string(value, enc_key)
        print('%s="%s"' % (key, dec_value))


def encrypt_env(env_path, password='', keyfile=''):
    enc_key = get_key(password, keyfile)

    values = dotenv.main.dotenv_values(env_path)
    for key, value in values.items():
        enc_value = encrypt_string(value, enc_key)
        dotenv.set_key(env_path, key, enc_value)
    return


def decrypt_env(env_path, password='', keyfile=''):
    enc_key = get_key(password, keyfile)

    values = dotenv.main.dotenv_values(env_path)
    for key, value in values.items():
        dec_value = decrypt_string(value, enc_key)
        dotenv.set_key(env_path, key, dec_value)
    return


def get_key(password, keyfile):
    if password is not None:
        key = password
    elif keyfile is not None:
        with open(keyfile, 'r') as f:
            key = f.read()
    else:
        raise ValueError("You must specify either a password or keyfile.")

    if key > 1024:
        key = key[:1024]

    salt = 'Er8iVILpk7CIoJU+C+N+ze+7/gAHfi9zHaT6vIzD6hk='
    enc_key = hashlib.pbkdf2_hmac('sha256', key, salt, 1000000)
    return enc_key


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
