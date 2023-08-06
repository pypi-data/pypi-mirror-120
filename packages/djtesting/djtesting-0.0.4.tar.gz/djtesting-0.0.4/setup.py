# -*- coding: utf-8 -*-
# @Time    : 2021/9/2 15:32
# @Author  : chinablue
# @Email   : dongjun@reconova.cn
# @File    : setup.py


import setuptools

requires = [
    'requests',
    'Faker',
    'allure-pytest',
    'objectpath'
]

setuptools.setup(
    name="djtesting",
    version="0.0.4",
    author="chinablue",
    author_email="chinablue@163.com",
    license="MIT",
    description="automated interface testing for business",
    packages=setuptools.find_packages(),
    platforms=["win10"],
    install_requires=requires,
)
