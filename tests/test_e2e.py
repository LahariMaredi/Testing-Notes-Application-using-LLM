import time
import allure
from pages.login_page import LoginPage
from pages.notes_page import NotesPage
from api.api_client import APIClient
from config.environment import config
from utils.screenshot import attach_screenshot_to_allure


@allure.feature("End-to-End")
@allure.story("UI Create Note and Verify via API")
def test_ui_api_flow(driver):

    login = LoginPage(driver)
    notes = NotesPage(driver)
    api = APIClient()

    title = f"Hybrid_{int(time.time())}"

    with allure.step("Open login page"):
        login.open(config["base_url"])
        attach_screenshot_to_allure(driver, "Login Page Loaded")

    with allure.step(f"Login with credentials"):
        login.login(config["email"], config["password"])
        attach_screenshot_to_allure(driver, "After Login")

    with allure.step(f"Create note via UI with title: {title}"):
        notes.click_add_note()
        notes.create_note(title, "UI + API")
        attach_screenshot_to_allure(driver, "Note Created in UI")

    with allure.step("Verify note via API"):
        api.login()
        response = api.get_notes().json()
        allure.attach(
            str(response),
            name="API Get Notes Response",
            attachment_type=allure.attachment_type.JSON
        )

    with allure.step(f"Assert note exists in API response"):
        titles = [n["title"] for n in response["data"]]
        assert title in titles
        allure.attach(
            f"Note found in API: {title}",
            name="Verification Result",
            attachment_type=allure.attachment_type.TEXT
        )
