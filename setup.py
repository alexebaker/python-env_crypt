import codecs

from setuptools import setup, find_packages


with open('requirements.txt') as f:
    requirements = f.read().splitlines()


setup(
    name="env_crypt",
    version="0.1.0",
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
    install_requires=requirements)
