from playwright.sync_api import Browser, BrowserContext, Page, Playwright


class BasePage:
    def __init__(self, playwright: Playwright, browser: Browser, context: BrowserContext, page: Page, base_url: str):
        self.playwright = playwright
        self.browser = browser
        self.context = context
        self.page = page
        self.base_url = base_url
        self.url = ""

    def load(self, url):
        full_url = f'{self.base_url}{url}'
        self.page.goto(full_url)

    def get_title(self):
        return self.page.title()

    def get_url(self):
        return self.page.url
