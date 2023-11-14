import json
import os
import time
from pathlib import Path

from playwright.sync_api import Playwright, sync_playwright

from plugins.logger import logger
from plugins.read_cases import ReadCases

from plugins.read_data import ReadData
from plugins.read_application import get_application_config

project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
cookie_path = Path(f"{project_path}/auth/cookies.json")


def login(playwright: Playwright) -> None:
    # todo 定位方式从yaml获取
    if cookie_path.exists():
        with open(cookie_path, "r") as file:
            data = json.load(file)
            cookies = data['cookies']  # 正确获取cookie列表
            current_time = time.time()
            if all(cookie.get("expires", 0) > current_time for cookie in cookies):
                return  # Cookie仍然有效，不需要再次登录
    read_data = ReadData('data/data.yaml')

    username = read_data.get_user_info()['username']
    password = read_data.get_user_info()['password']
    base_url = get_application_config()['base_url']
    # 如果cookie不存在或已过期，则执行登录流程
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    element_cases = ReadCases('data/cases/login.yaml').read_yaml()
    logger.info(f"login cases: {element_cases}")
    page.goto(f"{base_url}{element_cases['url']}")
    page.locator("//div[@class='system-text bottom']/div/span[text()='SMART_MSDW']").click()
    page.get_by_placeholder('请输入用户名', exact=True).fill(username)
    page.get_by_placeholder('请输入密码', exact=True).fill(password)
    page.locator("//span[text()='登 录']").click()
    page.locator(" //div/span[text()='管理员团队']/../../div[@class='product-content']").click()
    storage = context.storage_state(path=cookie_path)

    context.close()
    browser.close()


with sync_playwright() as p:
    login(p)
