#!/usr/bin/env python
#-*- coding:utf-8 -*-

#############################################
# File Name: setup.py
# Author: wby
# Mail: 1418885488@qq.com
# Created Time:  2018-9-1 00:55:34 AM
#############################################


from setuptools import setup, find_packages

setup(
    name = "wbyhome",
    version = "0.0.1",
    keywords = ("pip", "tool", "wbyhome"),
    description = "tool in subject",
    long_description = "wbyhome is tool in subject",
    license = "MIT Licence",

    url = "https://github.com/fengmm521/pipProject",
    author = "wby",
    author_email = "1418885488@qq.com",

    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = ['requests','lxml']
)