#!/usr/bin/python
# encoding=utf-8

"""
@Author  :  Lijiawei
@Date    :  8/24/2021 1:35 PM
@Desc    :  Scaffold Generator.
"""

import os
import platform
import sys

from loguru import logger


class ExtraArgument:
    create_venv = False


def init_parser_scaffold(subparsers):
    sub_parser_scaffold = subparsers.add_parser(
        "startproject", help="Create a new project with template structure."
    )
    sub_parser_scaffold.add_argument(
        "project_name", type=str, nargs="?", help="Specify new project name."
    )
    sub_parser_scaffold.add_argument(
        "-venv",
        dest="create_venv",
        action="store_true",
        help="Create virtual environment in the project, and install swaggerjmx-diff.",
    )
    return sub_parser_scaffold


def create_scaffold(project_name):
    """ Create scaffold with specified project name.
    """
    if os.path.isdir(project_name):
        logger.warning(
            f"Project folder {project_name} exists, please specify a new project name."
        )
        return 1
    elif os.path.isfile(project_name):
        logger.warning(
            f"Project name {project_name} conflicts with existed file, please specify a new one."
        )
        return 1

    logger.info(f"Create new project: {project_name}")
    print(f"Project root dir: {os.path.join(os.getcwd(), project_name)}\n")

    def create_folder(path):
        os.makedirs(path)
        msg = f"Created folder: {path}"
        print(msg)

    def create_file(path, file_content=""):
        with open(path, "w", encoding="utf-8") as f:
            f.write(file_content)
        msg = f"Created file: {path}"
        print(msg)

    create_folder(project_name)
    create_folder(os.path.join(project_name, "config"))
    create_folder(os.path.join(project_name, "data"))
    create_folder(os.path.join(project_name, "report"))
    create_folder(os.path.join(project_name, "tests"))

    content = """venv
.idea/
.pytest_cache
*/*__pycache__/
report
debug
*.pyc
"""
    create_file(os.path.join(project_name, ".gitignore"), content)

    content = """[pytest]
log_cli=true
log_cli_level=INFO
log_format = %(asctime)s [%(levelname)-5s] %(name)s %(funcName)s : %(message)s
log_date_format = %Y-%m-%d %H:%M:%S

# show all extra test summary info
addopts = -ra
testpaths = tests
python_files = test_diff.py
"""
    create_file(os.path.join(project_name, "pytest.ini"), content)

    content = """#!/usr/bin/python
# encoding=utf-8
\"\"\" Can only be modified by the administrator. Only Runner are provided.
\"\"\"
import pytest

from config.conf import *
from swaggerjmx_diff.tools import allure_report

if __name__ == '__main__':
    report_path = ALLURE_REPORT_PATH + os.sep + "result"
    report_html_path = ALLURE_REPORT_PATH + os.sep + "html"
    pytest.main(["-s", "--alluredir", report_path, "--clean-alluredir"])
    allure_report(report_path, report_html_path)
"""

    create_file(os.path.join(project_name, "run.py"), content)
    content = """#!/usr/bin/python
# encoding=utf-8
\"\"\" Can only be modified by the administrator. Only Data init are provided.
\"\"\"
from swaggerjmx_diff.tools import save_json, get_local_ip

from config.conf import DATA_PATH, ini

if __name__ == '__main__':
    version = save_json(swagger_url=get_local_ip(server_list=ini.getvalue('SERVER', 'ip').split(',')),
                        file_path=DATA_PATH)
    ini.update_value('VERSION', 'V', version)
"""
    create_file(os.path.join(project_name, "init.py"), content)

    content = """# Customize third-parties
# pip install --default-timeout=6000 -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

"""
    create_file(os.path.join(project_name, "requirements.txt"), content)

    content = """#!/usr/bin/python
# encoding=utf-8
\"\"\" Can only be modified by the administrator. Only Path are provided.
\"\"\"
import os

# 项目目录
from swaggerjmx_diff.tools import ReadConfig

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 配置文件
INI_PATH = os.path.join(BASE_DIR, 'config', 'config.ini')

# allure报告目录
ALLURE_REPORT_PATH = os.path.join(BASE_DIR, 'report')
if not os.path.exists(ALLURE_REPORT_PATH):
    os.mkdir(ALLURE_REPORT_PATH)
    
# data 接口数据目录
DATA_PATH = os.path.join(BASE_DIR, 'data')
if not os.path.exists(DATA_PATH):
    os.mkdir(DATA_PATH)
# 获取配置信息
ini = ReadConfig(INI_PATH)
"""

    create_file(os.path.join(project_name, "config", "conf.py"), content)

    content = """[VERSION]
v = 2021-09-21

[SERVER]
ip = http://ip:port/v2/api-docs, http://ip:port/v2/api-docs
"""
    create_file(os.path.join(project_name, "config", "config.ini"), content)
    create_file(os.path.join(project_name, "config", "__init__.py"))

    content = """#!/usr/bin/python
# encoding=utf-8
\"\"\" Can only be modified by the administrator. Only Cases are provided.
\"\"\"

import logging
import allure
import pytest

from swaggerjmx_diff.diff import contrast_swagger
from swaggerjmx_diff.tools import get_data, get_local_ip, read_json
from loguru import logger

from config.conf import ini, DATA_PATH


@allure.feature("Interface comparison test")
class TestApiDiff:
    @pytest.mark.parametrize("url", get_local_ip(server_list=ini.getvalue('SERVER', 'ip').split(',')))
    @allure.story("Interface diff test")
    @allure.title("{url}")
    @allure.description("Interface test comparison results")
    @allure.tag("Smoke testing")
    @allure.severity(allure.severity_level.TRIVIAL)
    def test_diff(self, url):

        expect_res, json_name = get_data(url=url)
        actual_res = read_json(json_name=json_name, file_path=DATA_PATH, version=ini.getvalue('VERSION', 'v'))
        logging.info('-------- 模块名 ---------')
        logging.info('')
        logging.info(json_name)
        logging.info('')
        logging.info('------ diff 结果 --------')
        logging.info('')
        contrast_result, result = contrast_swagger(result=actual_res, expected=expect_res)
        logging.info(contrast_result)
        logging.info('')
        logging.info('------------------------')
        try:
            assert result is True
        except AssertionError as e:
            logger.info(e)
            raise e

    if __name__ == "__main__":
        pytest.main(["-s", "test_diff.py"])
"""

    create_file(os.path.join(project_name, "tests", "test_diff.py"), content)
    create_file(os.path.join(project_name, "tests", "__init__.py"))

    if ExtraArgument.create_venv:
        os.chdir(project_name)
        print("\nCreating virtual environment")
        os.system("python -m venv venv")
        print("Created virtual environment: venv")

        print("Installing swaggerjmx-diff")
        if platform.system().lower() == 'windows':
            os.chdir("venv")
            os.chdir("Scripts")
            os.system("pip install swaggerjmx-diff")
        elif platform.system().lower() == 'linux':
            os.chdir("venv")
            os.chdir("bin")
            os.system("pip install swaggerjmx-diff")
        elif platform.system().lower() == 'mac':
            os.chdir("venv")
            os.chdir("bin")
            os.system("pip install swaggerjmx-diff")


def main_scaffold(args):
    ExtraArgument.create_venv = args.create_venv
    sys.exit(create_scaffold(args.project_name))
