# swaggerjmx-diff

[![Build Status](https://travis-ci.com/Pactortester/swaggerjmx-diff.svg?branch=master)](https://travis-ci.com/Pactortester/swaggerjmx-diff) ![PyPI](https://img.shields.io/pypi/v/swaggerjmx-diff) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/swaggerjmx-diff) ![GitHub top language](https://img.shields.io/github/languages/top/Pactortester/swaggerjmx-diff) ![PyPI - Downloads](https://img.shields.io/pypi/dm/swaggerjmx-diff?style=plastic) ![GitHub stars](https://img.shields.io/github/stars/Pactortester/swaggerjmx-diff?style=social) ![https://blog.csdn.net/flower_drop](https://img.shields.io/badge/csdn-%40flower__drop-orange)



## 安装


pip install -U swaggerjmx-diff


##  仓库地址：

- pypi：https://pypi.org/project/swaggerjmx-diff

## 功能


1. 对比2个 swagger json 是否有变化，监控 swagger的变动

## 快速开始
- 脚手架快速生成工程
```shell
swaggerjmx-diff startproject project_name
```
- 如下

![](https://files.mdnice.com/user/17535/0c5b12b2-765c-490e-84e2-24627447c09a.png)

## 二次开发

- 调用demo

```python
# -*- coding: utf-8 -*-

from swaggerjmx_diff.diff import *

with open('open-api-v1.json', 'r', encoding='utf8')as fp:
    json_data_v1 = json.load(fp)

with open('open-api-v2.json', 'r', encoding='utf8')as fp:
    json_data_v2 = json.load(fp)
    
contrast_result, result = contrast_swagger(json_data_v1, json_data_v2)

```
