import time
from pages.login_page import LoginPage
from pages.notes_page import NotesPage
from config.environment import config

def test_note_visible_without_refresh(driver):

    login = LoginPage(driver)
    notes = NotesPage(driver)

    login.open(config["base_url"])
    login.login(config["email"], config["password"])
    login.wait_for_login_success()

    title = f"Instant_{int(time.time())}"

    notes.click_add_note()
    notes.create_note(title, "Verify UI list updates instantly")

    assert notes.is_note_present(title)
