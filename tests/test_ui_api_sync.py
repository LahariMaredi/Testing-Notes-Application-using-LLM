import time
from pages.login_page import LoginPage
from pages.notes_page import NotesPage
from api.api_client import APIClient
from config.environment import config

def test_ui_api_sync(driver):
    """
    UI → API Sync:
    Create note via UI and verify it exists in API response
    """

    login = LoginPage(driver)
    notes = NotesPage(driver)
    api = APIClient()

    title = f"UI_API_{int(time.time())}"
    description = "created via UI"

    # Step 1: Login and create note via UI
    login.open(config["base_url"])
    login.login(config["email"], config["password"])
    login.wait_for_login_success()

    notes.click_add_note()
    notes.create_note(title, description)

    assert notes.is_note_present(title)

    # Step 2: Validate in API
    api.login()
    response = api.get_notes()

    assert response.status_code == 200

    notes_data = response.json().get("data", [])
    titles = [n["title"] for n in notes_data]

    assert title in titles, "UI created note not found in API"