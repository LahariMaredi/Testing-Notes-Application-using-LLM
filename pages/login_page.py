from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage

class LoginPage(BasePage):

    EMAIL = (By.CSS_SELECTOR, "input[data-testid='login-email']")
    PASSWORD = (By.CSS_SELECTOR, "input[data-testid='login-password']")
    LOGIN_BTN = (By.CSS_SELECTOR, "button[data-testid='login-submit']")

    # Primary error locator (data-testid preferred)
    ERROR_MESSAGE_PRIMARY = (By.CSS_SELECTOR, "[data-testid='alert-message']")
    # Fallback error locators
    ERROR_MESSAGE_FALLBACK = (By.CSS_SELECTOR, ".invalid-feedback, [role='alert'], .toast-body")

    def open(self, url):
        self.driver.get(url + "/login")
        self.wait.until(EC.visibility_of_element_located(self.EMAIL))

    def login(self, email, password):
        self.safe_type(self.EMAIL, email)
        self.safe_type(self.PASSWORD, password)
        self.safe_click(self.LOGIN_BTN)

    def wait_for_login_success(self):
        self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "button[data-testid='add-new-note']")))

    def get_error_message(self, error_text):
        """
        Wait for specific login error message using stable locators.
        Prefers data-testid, falls back to structured selectors.
        """
        try:
            # First try primary locator
            error_elements = self.driver.find_elements(*self.ERROR_MESSAGE_PRIMARY)
            for element in error_elements:
                if error_text in element.text:
                    return element
        except Exception:
            pass

        # Fallback to broader selectors
        self.wait.until(EC.visibility_of_any_elements_located(self.ERROR_MESSAGE_FALLBACK))
        locator = (
            By.XPATH,
            f"//*[contains(normalize-space(.), '{error_text}') and (contains(@class,'invalid-feedback') or @role='alert' or contains(@class,'toast-body'))]"
        )
        return self.wait.until(EC.visibility_of_element_located(locator))
