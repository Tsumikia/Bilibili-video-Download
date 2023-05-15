from setuptools import setup

setup(
    name='XXDown',
    version='1.0',
    description='A script for downloading videos from Bilibili',
    author='toyosaki',
    author_email='1518139129@qq.com',
    packages=[''],
    install_requires=[
        'jsonpath',
        'requests',
        'lxml',
        'DecryptLogin',
        'tqdm'
    ],
)
