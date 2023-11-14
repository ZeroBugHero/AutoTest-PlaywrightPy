import os

import pytest
from pathlib import Path

from playwright.sync_api import Playwright

from pages import login_page

project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
cookie_path = Path(f"{project_path}/auth/cookies.json")


# 异步的登录和设置会话状态 fixture
@pytest.fixture(scope="session", autouse=True)
def login(playwright: Playwright) -> None:
    login_page.login(playwright)


# 配置浏览器上下文参数的 fixture
@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    storage_state_path = Path(cookie_path)
    return {
        **browser_context_args,
        "storage_state": str(storage_state_path) if storage_state_path.exists() else None
    }
