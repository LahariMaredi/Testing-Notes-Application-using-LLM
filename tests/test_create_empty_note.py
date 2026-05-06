from pages.login_page import LoginPage
from pages.notes_page import NotesPage
from config.environment import config
from selenium.webdriver.common.by import By

def test_create_empty_note(driver):

    login = LoginPage(driver)
    notes = NotesPage(driver)

    login.open(config["base_url"])
    login.login(config["email"], config["password"])

    notes.click_add_note()
    notes.click(notes.CREATE_BTN)

    assert driver.find_element(By.XPATH, "//*[contains(text(),'Title is required')]").is_displayed()
    assert driver.find_element(By.XPATH, "//*[contains(text(),'Description is required')]").is_displayed()


def test_create_note_without_description(driver):

    login = LoginPage(driver)
    notes = NotesPage(driver)

    login.open(config["base_url"])
    login.login(config["email"], config["password"])

    notes.click_add_note()
    notes.type(notes.TITLE, "TestOnlyTitle")
    notes.click(notes.CREATE_BTN)

    assert driver.find_element(By.XPATH, "//*[contains(text(),'Description is required')]").is_displayed()
