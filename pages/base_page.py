from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from utils.wait_utils import safe_click, safe_type, wait_for_element_with_fallback

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def find(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    def click(self, locator):
        element = self.wait.until(EC.element_to_be_clickable(locator))
        try:
            element.click()
        except Exception:
            self.driver.execute_script("arguments[0].click();", element)

    def type(self, locator, text):
        element = self.find(locator)
        element.clear()
        element.send_keys(text)

    def find_with_fallback(self, primary_locator, fallback_locator, timeout=10):
        """
        Self-healing locator: Try primary locator first, fallback to secondary.
        """
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(primary_locator)
            )
        except Exception:
            return WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(fallback_locator)
            )

    def safe_click(self, locator):
        """Enhanced safe click using utility function."""
        safe_click(self.driver, locator)

    def safe_type(self, locator, text):
        """Enhanced safe type using utility function."""
        safe_type(self.driver, locator, text)
