import os

from playwright.sync_api import sync_playwright

from plugins.logger import logger
from utils.println import println


def check_browser_installation(browser_type: str = 'chromium') -> bool:
    """
    检查浏览器是否安装
    :param browser_type: 浏览器类型
    :return:  True or False
    """
    with sync_playwright() as playwright:
        chromium_path = playwright.chromium.executable_path
        print(chromium_path)
        firefox_path = playwright.firefox.executable_path
        webkit_path = playwright.webkit.executable_path

        if browser_type == 'chromium':
            return os.path.exists(chromium_path)
        elif browser_type == 'firefox':
            return os.path.exists(firefox_path)
        elif browser_type == 'webkit':
            return os.path.exists(webkit_path)
        else:
            logger.error(f'不支持浏览器类型的{browser_type}')
            raise ValueError(f"不支持浏览器类型的 '{browser_type}'。")


def install_browser():
    # 获取当前系统
    import platform
    system = platform.system()
    if system == 'Windows':
        println('yellow', "检测到当前系统为Windows")
        println('yellow', "正在安装浏览器客户端,请稍后...")
        os.system('playwright install')
    elif system == 'Linux' or system == 'Darwin':
        println('yellow', "检测到当前系统为Linux/Darwin")
        println('yellow', "正在安装浏览器客户端,请稍后...")
        os.system('playwright install')
    else:

        println('yellow', "未知系统,请手动安装浏览器客户端")
        println('yellow', "命令: playwright install")


if __name__ == '__main__':
    print(check_browser_installation())
