# ENV Crypt

[![License](http://img.shields.io/:license-mit-blue.svg)](https://github.com/alexebaker/python-env_crypt/blob/master/LICENSE)


Python module for encrypting and decryting .env files.


## Getting Started

This module can be installed with pythons setuptools. It is not currently in pypi, so just run setup.py locally:

```bash
python setup.py install
```

## Usage

After running the setup.py script, a cli tool called `env-crypt` is installed. This tool can be used for:

Encrypt the .env file with a password:

```bash
>>> env-crypt --env-path $PATH_TO_DOTENV --password $YOUR_PASSWORD encrypt
```

Decrypt the .env file with a password:

```bash
>>> env-crypt --env-path $PATH_TO_DOTENV --password $YOUR_PASSWORD decrypt
```

Encrypt the .env file with a keyfile:

```bash
>>> env-crypt --env-path $PATH_TO_DOTENV --keyfile $PATH_TO_SECRET_FILE encrypt
```

Decrypt the .env file with a password:

```bash
>>> env-crypt --env-path $PATH_TO_DOTENV --keyfile $PATH_TO_SECRET_FILE decrypt
```

You can update the value of an encrypted .env key without having to decrypt it first:

```bash
>>> env-crypt --env-path $PATH_TO_DOTENV --password $YOUR_PASSWORD update --key $KEY_TO_UPDATE --value $NEW_VALUE
```

You can see what the current values in the .env file are without having to decrypt and re-encrypt the files

```bash
>>> env-crypt --env-path $PATH_TO_DOTENV --keyfile $PATH_TO_SECRET_FILE list
```

Once you have encrypted you env file, you can load it into pythons environment by importing the module:

```python
import os
from env_crypt import load_env

load_env('path/to/.env', password='your password', keyfile='path/to/keyfile')

# Acees the env value as normal, it will be decrypted for use
os.environ[key]
```


## Author

[Alexander Baker](mailto:alexebaker@gmail.com)
