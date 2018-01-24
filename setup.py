import codecs
import re

from setuptools import setup, find_packages


def get_requirements():
    with open('requirements.txt') as f:
        requirements = f.read().splitlines()
    return requirements


def get_version():
    with open('env_crypt/version.py', 'r') as f:
        version = re.search(r'__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read())
    return version.group(1)


setup(
    name="env_crypt",
    version=get_version(),
    packages=find_packages(),
    url='https://github.com/alexebaker/python-env_crypt',
    author='Alexander Baker',
    author_email='alexebaker@gmail.com',
    description='Allows Encryption/Decryption of .env files.',
    keywords=['environment variables', 'settings', 'env', 'encryption',
              'dotenv', 'configurations', 'python'],
    long_description=codecs.open('README.md', encoding="utf8").read(),
    entry_points={
        'console_scripts': ['env-crypt=env_crypt.cli:run']},
    install_requires=get_requirements())
