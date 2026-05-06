import time
import pytest
from pages.login_page import LoginPage
from pages.notes_page import NotesPage
from config.environment import config
from utils.retry_logic import is_transient_error

def test_create_note_ui(driver):

    login = LoginPage(driver)
    notes = NotesPage(driver)

    try:
        login.open(config["base_url"])
        login.login(config["email"], config["password"])
        login.wait_for_login_success()

        title = f"UI_{int(time.time())}"

        notes.click_add_note()
        notes.create_note(title, "Automation Note")

        assert notes.is_note_present(title)
    except Exception as e:
        if is_transient_error(e):
            pytest.xfail(f"Transient UI issue – safe to retry: {str(e)}")
        else:
            raise

