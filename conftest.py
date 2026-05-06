import pytest
import allure
import logging
from fixtures.driver_fixture import driver
from api.api_client import APIClient
from utils.screenshot import take_screenshot
from utils.logger import setup_logger

logger = setup_logger(__name__)


@pytest.fixture
def api_client():
    api = APIClient()
    api.login()
    return api


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook to capture screenshot on test failure"""
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        if "driver" in item.fixturenames:
            driver = item.funcargs["driver"]
            screenshot_path = take_screenshot(driver, item.name)
            if screenshot_path:
                allure.attach.file(
                    screenshot_path,
                    name=f"Failure Screenshot - {item.name}",
                    attachment_type=allure.attachment_type.PNG
                )
                logger.error(f"Test failed. Screenshot saved: {screenshot_path}")


@pytest.fixture(scope="session", autouse=True)
def log_test_start(request):
    """Log test session start"""
    logger.info("=" * 80)
    logger.info("Test Session Started")
    logger.info("=" * 80)
    yield
    logger.info("=" * 80)
    logger.info("Test Session Completed")
    logger.info("=" * 80)
