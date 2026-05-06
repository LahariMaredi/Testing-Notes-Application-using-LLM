import allure
from pages.login_page import LoginPage
from config.environment import config
from utils.screenshot import attach_screenshot_to_allure


@allure.feature("Authentication")
@allure.story("User Login")
def test_login(driver):
    login = LoginPage(driver)

    with allure.step("Open login page"):
        login.open(config["base_url"])
        attach_screenshot_to_allure(driver, "Login Page")

    with allure.step(f"Login with email: {config['email']}"):
        login.login(config["email"], config["password"])
        attach_screenshot_to_allure(driver, "After Successful Login")

    with allure.step("Verify notes page URL"):
        current_url = driver.current_url
        assert "notes" in current_url.lower()
        allure.attach(
            f"Current URL: {current_url}",
            name="URL Verification",
            attachment_type=allure.attachment_type.TEXT
        )
