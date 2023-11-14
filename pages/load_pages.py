import re

from typing import Dict, List, Optional
from playwright.sync_api import Browser, BrowserContext, Page, Playwright

from pages.base_page import BasePage
from plugins.logger import logger
from plugins.network_listener import NetworkListener
from plugins.read_application import get_application_config

ElementsType = Dict[str, List[Dict[str, str]]]


class LoadPages(BasePage):
    is_network_listen = get_application_config()['is_network_listen']

    def __init__(self, playwright: Playwright, browser: Browser, context: BrowserContext, page: Page, base_url: str,
                 elements: ElementsType):
        """
            构造函数。
            参数:
                playwright (Playwright): Playwright 实例。
                browser (Browser): 浏览器实例。
                context (BrowserContext): 上下文实例。
                page (Page): 页面实例。
                base_url (str): 基础 URL。
                elements (elements_type): 元素的类型和属性。
            """
        super().__init__(playwright, browser, context, page, base_url)
        self.locator = None
        self.elements = elements
        self.cases = elements['elements']
        self.cases_type = elements['case']
        if self.is_network_listen:
            NetworkListener(self.page)
        logger.info(self.cases)

    def navigate(self):
        # 使用三元运算符将基于URL的条件简化为一行，以提高可读性。
        self.page.goto(f'{self.base_url}{self.elements["url"]}') if "url" in self.elements else logger.warning(
            "没有指定的URL进行导航.")
        if self.is_network_listen:
            self.page.wait_for_load_state("networkidle")  # 等待网络空闲

    def combo_locator(self, values: Dict[str, Optional[str]]):
        try:
            element_by_test_id = self.page.get_by_test_id(values['by_test_id'])
            if element_by_test_id is None:
                raise ValueError(f"无法通过 by_test_id='{values['by_test_id']}' 定位到元素")
            element_by_text = element_by_test_id.get_by_text(values['by_text'])
            if element_by_text is None:
                raise ValueError(f"无法通过 by_text='{values['by_text']}' 定位到元素")
            return element_by_text
        except Exception as e:
            logger.error(f"组合定位元素失败，错误信息为：{e}")
            raise  # 重新抛出异常，以停止后续操作

    def get_by_text_modify(self, values: Dict[str, Optional[str]]) -> object:
        """获取页面元素通过文本内容，可配置是否进行完全匹配。"""
        try:
            logger.info(f"get_by_text_modify,values为{values}")
            exact = values.get('exact')
            is_exact = exact in {"true", True, 1}
            logger.debug(f"是否完全匹配：{'true' if is_exact else 'false'}")

            element_by_text = self.page.get_by_text(values.get('by_text'), exact=True)

            if element_by_text is None:
                raise ValueError(f"无法通过 by_text='{values.get('by_text')}' 定位到元素")

            return element_by_text
        except Exception as e:
            logger.error(f"通过文本定位元素失败，错误信息为：{e}")
            raise  # 重新抛出异常，以停止后续操作

    def get_by_role_modify(self, values: dict) -> object:
        """获取页面元素通过角色属性，可配置是否进行完全匹配。"""
        try:
            logger.info(f"get_by_role_modify定位,values为{values}")
            exact = values.get('exact')
            is_exact = exact in {"true", True, 1}
            role_literal = values.get('role_literal')

            element_by_role = self.page.get_by_role(role_literal, name=values.get('by_text'), exact=is_exact)

            if element_by_role is None:
                raise ValueError(f"无法通过 role='{role_literal}' 和 by_text='{values.get('by_text')}' 定位到元素")

            return element_by_role
        except Exception as e:
            logger.error(f"通过角色定位元素失败，错误信息为：{e}")
            raise  # 重新抛出异常，以停止后续操作

    def get_by_label_modify(self, values: str) -> object:
        try:
            logger.info(f"get_by_label_modify,values为{values}")
            # 如果输入字符串包含'|'，则进行分割
            if "|" in values:
                label, locator = values.split("|", 1)  # 限制分割次数为1，避免多余的分割
                element_by_label = self.page.get_by_label(label).locator(locator)

                if element_by_label is None:
                    raise ValueError(f"无法通过 label='{label}' 和 locator='{locator}' 定位到元素")

                return element_by_label
            else:
                element_by_label = self.page.get_by_label(values)

                if element_by_label is None:
                    raise ValueError(f"无法通过 label='{values}' 定位到元素")

                return element_by_label
        except Exception as e:
            logger.error(f"通过标签定位元素失败，错误信息为：{e}")
            raise  # 重新抛出异常，以停止后续操作

    def get_by_regex_text(self, values: str) -> object:
        try:
            logger.info(f"get_by_regex_text,values为{values}")
            if "|" in values:
                tag, regex = values.split("|", 1)  # 限制分割次数为1，避免多余的分割
                element_by_regex = self.page.locator(tag).filter(has_text=re.compile(regex))

                if element_by_regex is None:
                    raise ValueError(f"无法通过 tag='{tag}' 和 regex='{regex}' 定位到元素")

                return element_by_regex
            else:
                raise ValueError(f"{values}的格式无效。期望的格式为：tag|regex")
        except Exception as e:
            logger.error(f"通过正则表达式定位元素失败，错误信息为：{e}")
            raise  # 重新抛出异常，以停止后续操作

    def locate_element(self, element: Dict[str, Optional[str]]):
        element_type = element.get('type', '')
        element_values = element.get('values', '')

        # 将相关的数据（常量）分组在一起，并与代码的其他部分分开。
        locator_method = {
            'placeholder': self.page.get_by_placeholder,
            'alt_text': self.page.get_by_alt_text,
            'xpath': self.page.locator,
            'test_id': self.page.get_by_test_id,
            # -----------------------以下是自定义定位方法-------------------------------------
            'text': self.get_by_text_modify,  # 自定义get_by_text方法，实现是否精准匹配
            'role': self.get_by_role_modify,
            'label': self.get_by_label_modify,
            'combo': self.combo_locator,  # 新增的组合定位方法
            'regex_text': self.get_by_regex_text,  # 正则定位
        }

        locate_func = locator_method.get(element_type)
        try:
            # 简化 if 条件 - 不需要单独的返回 None 语句
            self.locator = locate_func(element_values) if locate_func else None
        except Exception as e:
            logger.error(f'元素定位失败: {e}')
            raise

    def operate_element(self, element: Dict[str, str]):
        operation_type = element.get('operation')
        operation_func = {
            'click': self.locator.click,
            'enter': lambda: self.locator.press('Enter'),
            'right_click': lambda: self.locator.click(button='right'),  # 添加右键点击操作
            'hover': self.locator.hover,
            None: lambda: None,
        }.get(operation_type, lambda: self.locator.fill(operation_type))

        try:
            operation_func()
        except Exception as e:
            logger.error(f'元素操作失败: {e}')
            raise

    def operate_elements(self):
        # for element in self.cases:
        #     self.locate_element(element)
        #     self.operate_element(element)
        # --------- 对上面的更简洁的写法，需要更扎实的基础理解 --------------
        [self.locate_element(element) or self.operate_element(element) for element in self.cases]

    def operate_case(self):
        # 简化函数调用
        self.load(self.elements.get('url'))
        self.operate_elements()
