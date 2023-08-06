#!/usr/bin/python
# encoding=utf-8

"""
@Author  :  Lijiawei
@Date    :  8/17/2021 6:49 PM
@Desc    :  plugin.py
"""

import os
import shutil
import tempfile
import time

import allure_commons
from allure_commons.logger import AllureFileLogger
from allure_pytest.listener import AllureListener
from allure_pytest.plugin import cleanup_factory

allure_temp = tempfile.mkdtemp()


class Project:
    dir = ""


def pytest_sessionstart(session):
    Project.dir = session.config.cache.get("project_dir", None)
    if not Project.dir:
        # First time run, no pytest_cache
        cwd = os.getcwd()
        tests = cwd.find("tests")
        # tests
        if tests > 0:
            Project.dir = cwd[:cwd.find("tests")]
        # root
        else:
            Project.dir = cwd


def current_time():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))


class Plugin:
    @staticmethod
    def pytest_addoption(parser):
        parser.addoption(
            "--swaggerjmx-diff-reports",
            action="store_const",
            const=True,
            help="Create swaggerjmx-diff allure HTML reports."
        )

    @staticmethod
    def _tep_reports(config):
        if config.getoption("--swaggerjmx-diff-reports") and not config.getoption("allure_report_dir"):
            return True
        else:
            return False

    @staticmethod
    def pytest_configure(config):
        if Plugin._tep_reports(config):
            test_listener = AllureListener(config)
            config.pluginmanager.register(test_listener)
            allure_commons.plugin_manager.register(test_listener)
            config.add_cleanup(cleanup_factory(test_listener))

            clean = config.option.clean_alluredir
            file_logger = AllureFileLogger(allure_temp, clean)
            allure_commons.plugin_manager.register(file_logger)
            config.add_cleanup(cleanup_factory(file_logger))

    @staticmethod
    def pytest_sessionfinish(session):
        if Plugin._tep_reports(session.config):
            reports_dir = os.path.join(Project.dir, "reports")
            new_report = os.path.join(reports_dir, "report-" + current_time().replace(":", "-").replace(" ", "-"))
            if os.path.exists(reports_dir):
                his_reports = os.listdir(reports_dir)
                if his_reports:
                    latest_report_history = os.path.join(reports_dir, his_reports[-1], "history")
                    shutil.copytree(latest_report_history, os.path.join(allure_temp, "history"))
            os.system(f"allure generate {allure_temp} -o {new_report}  --clean")
            shutil.rmtree(allure_temp)
