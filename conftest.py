import allure
from pytest import Item

"""
借鉴/学习上海-悠悠大佬的方案
blog地址: https://www.cnblogs.com/yoyoketang/tag/python%2Bplaywright/
"""
# 本地插件注册
pytest_plugins = ['plugins.pytest_playwright', 'plugins.pytest_base_url']  # noqa


def pytest_addoption(parser):
    parser.addoption("--casepath", action="store")


def pytest_generate_tests(metafunc):
    if 'case_path' in metafunc.fixturenames:
        case_path = metafunc.config.getoption('casepath')
        if case_path:
            metafunc.parametrize("case_path", [case_path])


def pytest_runtest_call(item: Item):  # noqa
    # 动态添加测试类的 allure.feature()
    if item.parent._obj.__doc__:  # noqa
        allure.dynamic.feature(item.parent._obj.__doc__)
        # 动态添加测试用例的title 标题 allure.title()
    if item.function.__doc__:  # noqa
        allure.dynamic.title(item.function.__doc__)  # noqa
