#!/usr/bin/python
# encoding=utf-8

"""
@Author  :  Lijiawei
@Date    :  9/21/2021 1:32 PM
@Desc    :  diff.py
"""

import json

from deepdiff import DeepDiff
from loguru import logger


def contrast_swagger(result, expected):
    """

    :param result:
    :param expected:
    :return:
    """
    cmp_dict = DeepDiff(result, expected, ignore_order=True).to_dict()
    if expected is None:
        logger.error("The JSON passed in is empty, please check!")
        return None, False
    else:
        if cmp_dict.get("dictionary_item_added") or cmp_dict.get("dictionary_item_removed") or cmp_dict.get(
                "values_changed"):
            logger.info(cmp_dict)
            logger.info("Interface structure has transformation!")
            return cmp_dict, False
        else:
            return cmp_dict, True


def merge_swagger(add_str, new_json):
    """
    合并更新生成新的json
    :param add_str:
    :param new_json:
    :return:
    """

    global key
    add_str = add_str.replace('root', '')
    add_str = add_str.replace('[', '')
    add_str = add_str.replace("'", '')
    keys = add_str.split(']')[:-1]
    data = {}
    for key in reversed(keys):
        if not data:
            data[key] = None
        else:
            data = {key: data}
    value = None
    v_ref = data
    for item, key in enumerate(keys, 1):
        if not value:
            value = new_json.get(key)
        else:
            value = value.get(key)
        if item < len(keys):
            v_ref = v_ref.get(key)
    v_ref[key] = value
    return data


def format_swagger_v1(diff_result, latest_swagger):
    """

    :param latest_swagger: 最新的 swagger json
    :param diff_result:对比结果
    :return:格式化合并完成的 swagger json
    """
    added_dict = []
    try:
        add_result = diff_result['dictionary_item_added']

    except KeyError:
        logger.error('There is no new item in diff result!')
        return None
    for added_str in add_result:
        added_dict.append(merge_swagger(add_str=added_str, new_json=latest_swagger))

    new_list = []

    for i in added_dict:
        try:
            new_list.append(str(i['paths']).lstrip('{').replace('}}}}}', '}}}}'))
        except KeyError:
            pass
    latest_swagger['paths'] = {str(new_list).replace('["', '').replace('"]', '').replace('"', '')}
    merge_swagger_json = json.loads(
        str(latest_swagger).replace('"', '').replace("'", '"').replace('False', 'false').replace('True', 'true'))
    return merge_swagger_json


def format_swagger_v2(diff_result, latest_swagger):
    """

    :param latest_swagger: 最新的 swagger json
    :param diff_result:对比结果
    :return:格式化合并完成的 swagger json
    """
    added_dict = []
    try:
        add_result = diff_result['dictionary_item_added']

    except KeyError:
        logger.error('There is no new item in diff result!')
        return None
    for added_str in add_result:
        added_dict.append(merge_swagger(add_str=added_str, new_json=latest_swagger))

    new_list = []

    for i in added_dict:
        try:
            new_list.append(str(i['paths']).lstrip('{').replace('}}}}}', '}}}}'))
        except KeyError:
            pass
    latest_swagger['paths'] = {
        str(new_list).replace('["', '').replace('"]', '').replace('"', '').replace('}}},', '}},').replace('}}}}',
                                                                                                          '}}}').replace(
            'False', 'false').replace('True', 'true')}
    merge_swagger_json = json.loads(str(latest_swagger).replace('{"', '{').replace('}}}"}', '}}}').replace("'", '"'))
    return merge_swagger_json