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
        driver = item.funcargs.get("driver")
        if driver:
            screenshot_path = take_screenshot(driver, item.name)
            if screenshot_path:
                allure.attach.file(
                    screenshot_path,
                    name=f"Failure Screenshot - {item.name}",
                    attachment_type=allure.attachment_type.PNG
                )
                logger.error(f"Test failed. Screenshot saved: {screenshot_path}")

        if call.excinfo:
            error_message = str(call.excinfo.getrepr())
            
            # Trigger AI Root Cause Analysis
            from llm_automation.failure_analyzer import FailureAnalyzer
            try:
                logger.info(f"Triggering AI Analysis for {item.nodeid}...")
                analyzer = FailureAnalyzer()
                analysis_text = analyzer.analyze_failure(item.nodeid, error_message)
                allure.attach(
                    analysis_text,
                    name=f"AI Root Cause Analysis - {item.name}",
                    attachment_type=allure.attachment_type.TEXT
                )
            except Exception as e:
                logger.error(f"Failed to generate AI analysis: {e}")

            # Trigger AI Locator Suggestions
            locator_errors = ["NoSuchElementException", "TimeoutException", "ElementNotInteractable", "ElementClickIntercepted", "StaleElementReference"]
            if any(err in error_message for err in locator_errors):
                from llm_automation.locator_expert import LocatorExpert
                try:
                    logger.info(f"Triggering AI Locator Expert for {item.nodeid}...")
                    expert = LocatorExpert()
                    dom_source = driver.page_source if driver else ""
                    if dom_source:
                        suggestions = expert.suggest_locators(item.nodeid, error_message, dom_source)
                        allure.attach(
                            suggestions,
                            name=f"AI Locator Suggestions - {item.name}",
                            attachment_type=allure.attachment_type.TEXT
                        )
                except Exception as e:
                    logger.error(f"Failed to generate locator suggestions: {e}")


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
