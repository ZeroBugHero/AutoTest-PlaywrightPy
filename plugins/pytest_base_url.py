# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""
pytest 本地插件
pytest_base_url.py
"""
import os
import pytest
from plugins.read_application import get_application_config

"""

参考上海-悠悠的pytest_playwright.py的写法
"""


@pytest.fixture(scope="session")
def base_url(request):
    """Return a base URL"""
    return request.config.getoption("base_url")


@pytest.fixture(scope="session", autouse=True)
def _verify_url(request, base_url):
    """Verifies the base URL"""
    verify = request.config.option.verify_base_url
    if base_url and verify:
        # Lazy load requests to reduce cost for cases that don't use the plugin
        import requests
        from urllib3.util.retry import Retry
        from requests.adapters import HTTPAdapter

        session = requests.Session()
        retries = Retry(backoff_factor=0.1, status_forcelist=[500, 502, 503, 504])
        session.mount(base_url, HTTPAdapter(max_retries=retries))
        session.get(base_url)


def pytest_addoption(parser):
    parser.addini(
        "base_url",
        help="Base URL for the application under test. This option can also be set in a local config file.",
    )
    parser.addoption(
        "--base-url",
        metavar="url",
        help="Base URL for the application under test. This "
             "option overrides the one in pytest.ini and the local config file.",
    )
    parser.addoption(
        "--verify-base-url",
        action="store_true",
        default=not bool(os.getenv("VERIFY_BASE_URL", "false").lower() == "false"),
        help="Verify the base URL.",
    )


def pytest_configure(config):
    base_url = config.getoption("base_url") or config.getini("base_url")
    if not base_url:
        base_url = get_application_config().get("base_url")

    # Set the base URL in the config
    config.option.base_url = base_url

    # Add the base URL to the metadata
    if hasattr(config, "_metadata"):
        config._metadata["Base URL"] = base_url


def pytest_report_header(config, startdir):
    base_url = config.getoption("base_url")
    if base_url:
        return f"baseurl: {base_url}"
