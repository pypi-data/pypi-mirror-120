#!/usr/bin/env python
# -*- coding:utf-8 -*-
from setuptools import setup, find_packages

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="swaggerjmx-diff",
    version="1.0.2",
    keywords=["pip", "swaggerjmx-diff", "swaggerjmx", "diff"],
    description="swaggerjmx-diff",
    long_description=long_description,
    long_description_content_type='text/markdown',
    license="MIT Licence",

    url="https://github.com/Pactortester",
    author="lijiawei",
    author_email="1456470136@qq.com",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console :: Curses",
        "Operating System :: MacOS",
        "Operating System :: POSIX",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Security",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: Proxy Servers",
        "Topic :: System :: Networking :: Monitoring",
        "Topic :: Software Development :: Testing",
        "Typing :: Typed",
    ],

    entry_points="""
    [console_scripts]
    swaggerjmx-diff = swaggerjmx_diff.cli.cli:main
    """,
    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=["deepdiff~=5.5.0", "loguru~=0.5.3", "allure-pytest~=2.9.43", "allure-python-commons~=2.9.43",
                      "requests~=2.25.1"]
)
