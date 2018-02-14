from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import

import os
import dotenv
import base64
import hashlib

from Crypto.Cipher import AES
from Crypto import Random


def load_env(env_path, password='', keyfile=''):
    """Decrypt the env vars and load them into the environment.

    Args:
        env_path (string): Path to the .env file to load.
        password (string): Password used to encrypt the .env file.
        keyfile (string): File used to encrypt the .env file.

    Example:
        >>> import os
        >>> from env_crypt import load_env
        >>> load_env('test.env', password='secret password')
        >>> print(os.environ['env key'])
    """
    dotenv.load_dotenv(env_path)
    salt = dotenv.get_key(env_path, 'salt')
    enc_key, _ = get_enc_key(password, keyfile, salt=salt)
    values = dotenv.main.dotenv_values(env_path)
    for key in values.keys():
        if key != 'salt':
            os.environ[key] = decrypt_string(os.environ[key], enc_key)
    return


def update_env(env_path, key='', value='', password='', keyfile=''):
    """Update a value in an encrypted .env file.

    This will encrypt the new value using the password or keyfile.

    Args:
        env_path (string): Path to the .env file to load.
        key (string): Name of the key to update.
        value (string): Updated value to set to the key.
        password (string): Password used to encrypt the .env file.
        keyfile (string): File used to encrypt the .env file.

    Example:
        >>> import os
        >>> from env_crypt import load_env
        >>> update_env('test.env', key='key', value='new value', password='secret password')
    """
    if key is None or value is None:
        raise ValueError("You must specify a key and a value"
                         " to update the env file.")

    salt = dotenv.get_key(env_path, 'salt')
    enc_key, _ = get_enc_key(password, keyfile, salt=salt)
    enc_value = encrypt_string(value, enc_key)
    dotenv.set_key(env_path, key, enc_value)
    return


def list_env(env_path, password='', keyfile=''):
    """Decrypt and list the values in the .env file.

    Args:
        env_path (string): Path to the .env file to load.
        password (string): Password used to encrypt the .env file.
        keyfile (string): File used to encrypt the .env file.

    Example:
        >>> import os
        >>> from env_crypt import list_env
        >>> load_env('test.env', password='secret password')
        key1=value1
        key2=value2
        etc...
    """
    salt = dotenv.get_key(env_path, 'salt')
    enc_key, _ = get_enc_key(password, keyfile, salt=salt)
    values = dotenv.main.dotenv_values(env_path)
    for key, value in values.items():
        if key != 'salt':
            dec_value = decrypt_string(value, enc_key)
        else:
            dec_value = value
        print('%s="%s"' % (key, dec_value))
    return


def encrypt_env(env_path, password='', keyfile=''):
    """Encrypt a .env file.

    Args:
        env_path (string): Path to the .env file to load.
        password (string): Password used to encrypt the .env file.
        keyfile (string): File used to encrypt the .env file.

    Example:
        >>> import os
        >>> from env_crypt import encrypt_env
        >>> encrypt_env('test.env', password='secret password')
    """
    enc_key, salt = get_enc_key(password, keyfile)

    values = dotenv.main.dotenv_values(env_path)
    for key, value in values.items():
        enc_value = encrypt_string(value, enc_key)
        dotenv.set_key(env_path, key, enc_value)
    dotenv.set_key(env_path, 'salt', salt)
    return


def decrypt_env(env_path, password='', keyfile=''):
    """Decrypt a .env file.

    Args:
        env_path (string): Path to the .env file to load.
        password (string): Password used to encrypt the .env file.
        keyfile (string): File used to encrypt the .env file.

    Example:
        >>> import os
        >>> from env_crypt import decrypt_env
        >>> decrypt_env('test.env', password='secret password')
    """
    salt = dotenv.get_key(env_path, 'salt')
    dotenv.unset_key(env_path, 'salt')
    enc_key, _ = get_enc_key(password, keyfile, salt=salt)

    values = dotenv.main.dotenv_values(env_path)
    for key, value in values.items():
        dec_value = decrypt_string(value, enc_key)
        dotenv.set_key(env_path, key, dec_value)
    return


def get_enc_key(password, keyfile, salt=None):
    """Get a secure key used for encryption/decryption.

    If both password and keyfile are given, only the password will be used.

    Args:
        password (string): Password used to encrypt the .env file.
        keyfile (string): File used to encrypt the .env file.
        salt (string): Salt to use for generating the encryption key.
            If this is not given, a random one will be used and returned.

    Returns:
        A tuple (enc_key, salt) of the encryption key
        and the salt used to generate the encryption key.

    Example:
        >>> import os
        >>> from env_crypt import get_enc_key
        >>> get_enc_key('secret password', None, salt='long and random')
        (enc_key, salt)
    """
    if password:
        key = password
    elif keyfile:
        with open(os.path.expanduser(keyfile), 'rb') as f:
            key = f.read()
    else:
        raise ValueError("You must specify either a password or keyfile.")

    if key > 1024:
        key = key[:1024]

    if salt is None:
        salt = Random.new().read(256)
    else:
        salt = base64.b64decode(salt)

    enc_key = hashlib.pbkdf2_hmac('sha256', key, salt, 100000)
    return enc_key, base64.b64encode(salt)


def encrypt_string(plaintext, key):
    """Encrypt the given string with the given key.

    Args:
        plaintext (string): String to encrypt.
        key (string): Key to use for encryption.

    Returns:
        An encrypted string.

    Example:
        >>> import os
        >>> from env_crypt import encrypt_string
        >>> encrypt_string('plaintext', 'long and random')
    """
    iv = Random.new().read(AES.block_size)
    aes = AES.new(key, AES.MODE_CFB, iv)

    ciphertext = base64.b64encode(iv + aes.encrypt(plaintext))
    return ciphertext


def decrypt_string(ciphertext, key):
    """Decrypt the given string with the given key.

    Args:
        ciphertext (string): String to decrypt.
        key (string): Key to use for decryption.

    Returns:
        A decrypted string.

    Example:
        >>> import os
        >>> from env_crypt import decrypt_string
        >>> decrypt_string('ciphertext', 'long and random')
    """
    ciphertext = base64.b64decode(ciphertext)
    iv = ciphertext[:AES.block_size]
    aes = AES.new(key, AES.MODE_CFB, iv)

    plaintext = aes.decrypt(ciphertext[AES.block_size:])
    return plaintext
