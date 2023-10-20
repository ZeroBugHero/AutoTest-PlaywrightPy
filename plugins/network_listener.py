"""
@file:network_listener.py
"""
from playwright.sync_api import Page, sync_playwright

from plugins.logger import logger


class NetworkListener:

    def __init__(self, page: Page):
        self.page = page
        self.page.route('**/*', self._intercept_request)
        self.page.on("response", self._handle_response)

    def _intercept_request(self, route, request):
        logger.info(f"Intercepted request: {request.url}")
        logger.info(f"Intercepted request method: {request.method}")
        route.continue_()

    def _handle_response(self, response):
        logger.info(f"Received response: {response.url}")
        logger.info(f"Response status: {response.status}")

        # We need the sync variant to prevent the error
        try:
            response_text = response.text()
            logger.info(f"Response text: {response_text}")
        except UnicodeDecodeError:
            logger.warning(f"Failed to fetch response text: non-textual response")


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        # 注册网络请求监听器

        listener = NetworkListener(page)
        # 打开网页
        page.goto("https://www.baidu.com")

        # ... 其他操作

        browser.close()


if __name__ == "__main__":
    main()
