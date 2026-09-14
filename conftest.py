"""
Shared Pytest fixtures.

The `driver` fixture is the backbone of the framework: it spins up a fresh
browser session per test (so tests don't leak state into each other) and
guarantees teardown even if the test fails.

The `pytest_runtest_makereport` hook auto-captures a screenshot on any
test failure - useful evidence for bug reports and for a portfolio piece
(it shows you think about diagnosability, not just green/red results).
"""

import os
from datetime import datetime

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions

from utils import config

SCREENSHOT_DIR = os.path.join(os.path.dirname(__file__), "reports", "screenshots")


def pytest_addoption(parser):
    parser.addoption(
        "--browser", action="store", default=config.BROWSER,
        help="Browser to run tests in: chrome or firefox",
    )
    parser.addoption(
        "--headless", action="store", default=str(config.HEADLESS),
        help="Run browser headless: true or false",
    )


@pytest.fixture
def driver(request):
    browser = request.config.getoption("--browser")
    headless = request.config.getoption("--headless").lower() == "true"

    if browser == "chrome":
        options = ChromeOptions()
        if headless:
            options.add_argument("--headless=new")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        drv = webdriver.Chrome(options=options)
    elif browser == "firefox":
        from selenium.webdriver.firefox.options import Options as FirefoxOptions
        options = FirefoxOptions()
        if headless:
            options.add_argument("--headless")
        drv = webdriver.Firefox(options=options)
    else:
        raise ValueError(f"Unsupported browser: {browser}")

    drv.implicitly_wait(config.IMPLICIT_WAIT)

    yield drv

    drv.quit()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Attach a screenshot to any failed test that used the `driver` fixture."""
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        driver_fixture = item.funcargs.get("driver")
        if driver_fixture is not None:
            os.makedirs(SCREENSHOT_DIR, exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
            safe_name = item.name.replace("/", "_")
            path = os.path.join(SCREENSHOT_DIR, f"{safe_name}-{timestamp}.png")
            driver_fixture.save_screenshot(path)
            print(f"\nScreenshot saved on failure: {path}")
