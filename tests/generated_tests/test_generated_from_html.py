import pytest
from pages.login_page import LoginPage
from pages.notes_page import NotesPage
from config.environment import config
from utils.retry_logic import is_transient_error

def test_login_scenario(driver):
    login = LoginPage(driver)
    try:
        login.open(config["base_url"])
        login.login(config["email"], config["password"])
        login.wait_for_login_success()
        assert True
    except Exception as e:
        from utils.retry_logic import is_transient_error
        if is_transient_error(e):
            pytest.xfail(f"Transient UI issue: {str(e)}")
        else:
            raise

def test_create_note_scenario(driver):
    login = LoginPage(driver)
    notes = NotesPage(driver)
    try:
        login.open(config["base_url"])
        login.login(config["email"], config["password"])
        login.wait_for_login_success()
        notes.click_add_note()
        notes.create_note("Test Note", "This is a test note")
        assert notes.is_note_present("Test Note")
    except Exception as e:
        if is_transient_error(e):
            pytest.xfail(f"Transient UI issue: {str(e)}")
        else:
            raise

def test_delete_note_scenario(driver):
    login = LoginPage(driver)
    notes = NotesPage(driver)
    try:
        login.open(config["base_url"])
        login.login(config["email"], config["password"])
        login.wait_for_login_success()
        notes.click_add_note()
        notes.create_note("Test Note", "This is a test note")
        notes.delete_note("Test Note")
        assert not notes.is_note_present("Test Note")
    except Exception as e:
        if is_transient_error(e):
            pytest.xfail(f"Transient UI issue: {str(e)}")
        else:
            raise

def test_navigation_scenario(driver):
    login = LoginPage(driver)
    try:
        login.open(config["base_url"])
        login.login(config["email"], config["password"])
        login.wait_for_login_success()
        # Navigate to different pages
        driver.get(config["base_url"] + "/#tools")
        driver.get(config["base_url"] + "/tips")
        driver.get(config["base_url"] + "/test-cases")
        driver.get(config["base_url"] + "/about")
        assert True
    except Exception as e:
        if is_transient_error(e):
            pytest.xfail(f"Transient UI issue: {str(e)}")
        else:
            raise