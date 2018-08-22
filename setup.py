# coding: utf-8

from setuptools import setup, find_packages
import sys

if sys.version_info[0] == 3 and sys.version_info[1] >= 5:
    setup(
        name='simpati',
        version='0.1.0',
        author='HeathKang',
        author_email='heath.kang@foxmail.com',
        description='a lib to communicate with weiss simpati software',
        packages=find_packages(exclude=[]),
        include_package_data=True,
        license='MIT',
    )

