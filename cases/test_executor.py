import pytest

from pages.assertion_load import AssertionLoad
from pages.load_pages import LoadPages
from plugins.read_application import get_application_config
from plugins.read_cases import ReadCases


class TestExecutor:

    def test_executor(self, playwright, browser, context, page, case_path):
        base_url = get_application_config().get("base_url")
        elements = ReadCases(case_path=case_path).read_yaml()
        load_cases = LoadPages(playwright, browser, context, page, base_url, elements)
        load_cases.operate_case()
        AssertionLoad(page, elements).assertion()
        page.pause()
