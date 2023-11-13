"""
@file:network_listener.py
"""
from playwright.sync_api import Page, sync_playwright
from urllib.parse import urlparse, parse_qs

from plugins.logger import logger


class NetworkListener:

    def __init__(self, page: Page):
        self.page = page
        self.page.route('**/*', self._intercept_request)
        self.page.on("response", self._handle_response)

    def _intercept_request(self, route, request):
        resource_type = request.resource_type
        # 定义要过滤的静态资源类型
        ignored_types = {'image', 'stylesheet', 'script', 'font'}
        if resource_type.lower() not in ignored_types:
            # 仅对非静态资源打印详细信息
            logger.info(f"Intercepted request: {request.url}")
            logger.info(f"Intercepted request method: {request.method}")
            if request.method == "POST":
                logger.info(f"Request post data: {request.post_data}")
            else:
                # 解析请求的 URL 来获取参数
                parsed_url = urlparse(request.url)
                params = parse_qs(parsed_url.query)
                logger.info(f"Request params: {params}")

        route.continue_()

    def _handle_response(self, response):
        # 获取与响应关联的请求对象
        resource_type = response.request.resource_type
        ignored_types = {'image', 'stylesheet', 'script', 'font', "document"}
        if resource_type.lower() not in ignored_types:
            # 仅对非静态资源打印详细信息
            logger.info(f"Received response for: {response.url}")
            logger.info(f"Response status: {response.status}")

            try:
                response_text = response.text()
                logger.info(f"Response text: {response_text}")
            except Exception as e:
                logger.warning(f"Failed to fetch response text: {e}")


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        # 注册网络请求监听器

        listener = NetworkListener(page)
        # 打开网页
        page.goto("http://172.16.12.151/mrpv2")
        page.wait_for_load_state("networkidle")  # 等待网络空闲

        # ... 其他操作

        browser.close()


if __name__ == "__main__":
    main()
