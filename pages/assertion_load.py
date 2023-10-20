from typing import Any, Dict, List, Optional

from playwright.sync_api import Page, TimeoutError, expect

from plugins.logger import logger  # 假设这里有一个名为logger的日志模块
from utils.custom_exception import ElementNotFoundError
from utils.function_replacer import replace_functions

AssertionType = Dict[str, List[Dict[str, Any]]]  # 定义assertion_type为一个嵌套字典


class AssertionLoad:
    VALID_LOCATE_TYPES = ['xpath', 'placeholder', 'role', 'title', 'url']

    def __init__(self, page: Page, elements: AssertionType):
        self.page = page
        self.assertions = elements.get('expect')
        if self.assertions is None:
            logger.info("在元素中没有找到 'expect' 键，跳过断言。")
            return

    def get_locator(self, timeout: int, order: int, locate_type: str, locate_element: Optional[str] = None,
                    expected_value: Optional[str] = None) -> Optional[Any]:
        if locate_type not in self.VALID_LOCATE_TYPES:
            logger.error(f"无效的定位类型。必须是以下之一：{', '.join(self.VALID_LOCATE_TYPES)}")
            raise ValueError(f"无效的定位类型。必须是以下之一：{', '.join(self.VALID_LOCATE_TYPES)}")

        locator = None
        try:
            if locate_type == 'role':
                locator = self.page.get_by_role(locate_element).nth(order)
            elif locate_type == 'xpath':
                locator = self.page.wait_for_selector(locate_element, timeout=timeout)
            elif locate_type == 'placeholder':
                locator = self.page.wait_for_selector(f'[placeholder="{locate_element}"]', timeout=timeout)
            # ...（处理其他类型的定位）
        except TimeoutError:
            logger.error(f"获取元素超时，定位类型：{locate_type}, 定位元素：{locate_element}, 期望值：{expected_value}")
            raise ElementNotFoundError("无法找到元素")

        return locator

    def assertion(self):
        if self.assertions is None:
            logger.info("没有要执行的断言，跳过。")
            return

        for assertion in self.assertions:
            element_info = assertion.get('element')
            assertion_info = assertion.get('assertion')
            # 更新函数
            if 'expected_value' in assertion_info:
                assertion_info['expected_value'] = replace_functions(assertion_info.get('expected_value'))

            locate_type = element_info.get('locate_type')
            locate_element = element_info.get('role_literal')  # 或其他相应的字段
            expected_value = assertion_info.get('expected_value')  # 获取 expected_value
            timeout = element_info.get('timeout', 60)
            order = assertion_info.get('order', 0)
            if timeout:
                timeout = timeout * 1000
            try:
                locator = self.get_locator(locate_type=locate_type, locate_element=locate_element,
                                           expected_value=expected_value, timeout=timeout, order=order)
                check_assertion(assertion_method=assertion_info.get('method'), locator=locator,
                                expected_value=expected_value, timeout=timeout)
            except ElementNotFoundError as e:
                logger.error(f"元素未找到: {e}")


def check_assertion(assertion_method: str, timeout: int, locator: Any, expected_value: Optional[Any] = None):
    if locator is None:
        logger.error(f"{assertion_method} 断言失败。期望值：{expected_value}, 实际值：None")
        raise AssertionError(f"{assertion_method} 断言失败。期望值：{expected_value}, 实际值：None")
    try:
        if assertion_method == 'to_have_text':
            expect(locator).to_have_text(expected_value, timeout=timeout)
        elif assertion_method == 'to_have_text':
            expect(locator).not_to_have_text(expected_value)
        # ... 其他断言逻辑，例如：
        elif assertion_method == 'is_disabled':
            expect(locator).to_be_disabled()
        elif assertion_method == 'is_enabled':
            expect(locator).not_to_be_disabled()
        # ...

        logger.info(f"断言方式：{assertion_method} ,期望值：{expected_value}")
    except Exception as e:
        logger.error(f"{assertion_method} 断言失败。期望值：{expected_value}, 错误信息：{str(e)}")
        raise  # 如果你想在断言失败时停止测试，可以再次抛出这个异常
