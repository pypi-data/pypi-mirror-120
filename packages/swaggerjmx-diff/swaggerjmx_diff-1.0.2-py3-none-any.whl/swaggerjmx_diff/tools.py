#!/usr/bin/python
# encoding=utf-8

"""
@Author  :  Lijiawei
@Date    :  9/21/2021 1:49 PM
@Desc    :  tools.py
"""
import configparser
import json
import os
import subprocess
import time

import allure
import requests
from loguru import logger


def save_json(swagger_url, file_path):
    """
    根据 swagger_ip 获取json文件
    :param file_path:
    :param swagger_url: https://ip:port/v2/api-docs
    :return: 每个 url 对应的 json 文件
    """
    version = time.strftime("%Y-%m-%d")
    path = '{}/{}'.format(file_path, version)
    os.makedirs(path, exist_ok=True)
    for url in swagger_url:
        try:
            response = requests.get('{}'.format(url))
            data = json.loads(response.text)
            title = data.get("info")["title"]
            with open("{}/{}.json".format(path, title), 'w', encoding='utf-8') as fp:
                fp.write(json.dumps(data, indent=4, ensure_ascii=False))
        except Exception as E:
            logger.info('{}'.format(url) + str(E))
            pass

    return version
    # ini.update_value('VERSION', 'V', version)


@allure.step('获取本地基准版本接口数据')
def read_json(json_name, file_path, version):
    """
    读取json文件
    :param version:
    :param file_path:
    :param json_name: 文件名
    :return:
    """
    path = file_path + '/{}/'.format(version) + json_name
    with open(path, 'r', encoding='utf8')as fp:
        json_data = json.load(fp)
    return json_data


@allure.step('获取远程最新版本接口数据')
def get_data(url):
    """
    获取响应json
    :param url:请求地址
    :return:
    """
    response = requests.get(url)
    data = json.loads(response.text)
    title = data.get("info")["title"] + '.json'
    logger.info(title)
    return data, title


def get_local_ip(server_list):
    url_list = []
    # server_list = ini.getvalue('IM-SERVER', 'ip').split(',')
    # for i in server_list:
    #     ip = 'http://' + i + '/v2/api-docs?group=default-all'
    #     url_list.append(ip)
    for i in server_list:
        url_list.append(i)
    logger.info(url_list)
    return url_list


def allure_report(report_path, report_html):
    """
    生成allure 报告
    :param report_path:
    :param report_html:
    :return:
    """
    # 执行命令 allure generate
    allure_cmd = "allure generate %s -o %s --clean" % (report_path, report_html)
    try:
        subprocess.call(allure_cmd, shell=True)
    except Exception:
        logger.error("执行用例失败，请检查一下测试环境相关配置")
        raise


class ReadConfig:
    """配置文件"""

    def __init__(self, ini_path):
        self.ini_path = ini_path
        if not os.path.exists(ini_path):
            raise FileNotFoundError("配置文件%s不存在！" % ini_path)
        self.config = configparser.RawConfigParser()  # 当有%的符号时请使用Raw读取
        self.config.read(ini_path, encoding='utf-8')

    def _get(self, section, option):
        """获取"""
        return self.config.get(section, option)

    def _set(self, section, option, value):
        """更新"""
        self.config.set(section, option, value)
        with open(self.ini_path, 'w') as f:
            self.config.write(f)

    def getvalue(self, env, name):
        return self._get(env, name)

    def update_value(self, env, name, value):
        return self._set(env, name, value)