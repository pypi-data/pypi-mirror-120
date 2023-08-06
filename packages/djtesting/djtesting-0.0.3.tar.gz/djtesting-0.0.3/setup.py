# -*- coding: utf-8 -*-
# @Time    : 2021/9/2 15:32
# @Author  : chinablue
# @Email   : dongjun@reconova.cn
# @File    : setup.py


import setuptools

requires = [
    'requests>=2.26.0; python_version >= "3"',
    'Faker>=8.13.2; python_version >= "3"',
    'allure-pytest>=2.9.43; python_version >= "3"',
    'objectpath>=0.6.1; python_version >= "3"',
]

setuptools.setup(
    name="djtesting",
    version="0.0.3",
    author="chinablue",
    author_email="chinablue@163.com",
    license="MIT",
    description="automated interface testing for business",
    packages=setuptools.find_packages(),
    platforms=["win10"],
    install_requires=requires,
)
