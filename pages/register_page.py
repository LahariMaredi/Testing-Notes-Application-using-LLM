from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class RegisterPage(BasePage):

    EMAIL = (By.XPATH, "//input[@type='email']")
    NAME = (By.XPATH, "//input[@placeholder='Name']")
    PASSWORD = (By.XPATH, "//input[@type='password']")
    CONFIRM = (By.XPATH, "//input[@placeholder='Confirm Password']")
    REGISTER = (By.XPATH, "//button[contains(text(),'Register')]")

    def open(self, url):
        self.driver.get(url + "/register")

    def register(self, email, name, password):
        self.type(self.EMAIL, email)
        self.type(self.NAME, name)
        self.type(self.PASSWORD, password)
        self.type(self.CONFIRM, password)
        self.click(self.REGISTER)
