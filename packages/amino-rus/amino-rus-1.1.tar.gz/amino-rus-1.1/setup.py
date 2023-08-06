from setuptools import setup
version  = "1.1"
long_description = """
Асинхронная библиотека для взаимодействия с https://aminoapps.com/api и https://service.narvii.com/api/v1, собранная в одном файле. Все функции имеют русскоязычные имена.
"""
setup(
    name = 'amino-rus',
    version = '1.1',
    url = 'https://github.com/D4rkwat3r/amino-rus',
    download_url = 'https://github.com/D4rkwat3r/amino-rus/archive/refs/heads/main.zip',
    author = 'Darkwater',
    author_email = 'ktoya170214@gmail.com',
    description = 'Асинхронная русскоязычная библиотека для взаимодействия с API Amino',
    long_description = long_description,
    keywords = [
        'aminoapps',
        'amino',
        'amino-rus',
        'amino_rus',
        'amino-bot',
        'amino_bot',
        'amino-py',
        'amino_py',
        'amino.py',
        'narvii',
        'api',
    ],
    install_requires = [
        'setuptools',
        'aiohttp'
    ],
    setup_requires = [
        'wheel'
    ],
    packages = ['амино']
)