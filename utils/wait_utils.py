from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException

def safe_click(driver, locator, timeout=10):
    """
    Safely click an element with retry logic for transient failures.
    """
    wait = WebDriverWait(driver, timeout)
    try:
        element = wait.until(EC.element_to_be_clickable(locator))
        element.click()
    except Exception:
        # Fallback: wait again and try JavaScript click
        try:
            element = wait.until(EC.element_to_be_clickable(locator))
            driver.execute_script("arguments[0].click();", element)
        except Exception:
            raise

def safe_type(driver, locator, text, timeout=10):
    """
    Safely type text into an element with retry logic.
    """
    wait = WebDriverWait(driver, timeout)
    try:
        element = wait.until(EC.visibility_of_element_located(locator))
        element.clear()
        element.send_keys(text)
    except Exception:
        # Fallback: wait again and retry
        try:
            element = wait.until(EC.visibility_of_element_located(locator))
            element.clear()
            element.send_keys(text)
        except Exception:
            raise

def wait_for_element_with_fallback(driver, primary_locator, fallback_locator=None, timeout=10):
    """
    Wait for element with primary locator, fallback to secondary if provided.
    """
    wait = WebDriverWait(driver, timeout)
    try:
        return wait.until(EC.visibility_of_element_located(primary_locator))
    except TimeoutException:
        if fallback_locator:
            return wait.until(EC.visibility_of_element_located(fallback_locator))
        raise
