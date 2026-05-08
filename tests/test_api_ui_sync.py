import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from api.api_client import APIClient
from pages.login_page import LoginPage
from pages.notes_page import NotesPage
from config.environment import config

def test_api_ui_delete_sync(driver):
 

    api = APIClient()
    api.login()

   
    title = f"API_DEL_{int(time.time())}"
    create = api.create_note(title, "temp note")
    assert create.status_code in [200, 201]

    note_id = create.json()["data"]["id"]

    delete = api.delete_note(note_id)
    assert delete.status_code in [200, 204]

    # Wait for backend to process
    time.sleep(1)

    # Step 3: Open UI
    login = LoginPage(driver)
    notes = NotesPage(driver)

    login.open(config["base_url"])
    login.login(config["email"], config["password"])
    login.wait_for_login_success()

    # Step 4: Refresh UI
    driver.refresh()

    # Step 5: Wait for note to be removed from UI
    note_locator = (By.XPATH, f"//div[@data-testid='note-card-title' and normalize-space(text())='{title}']")
    notes.wait.until(EC.invisibility_of_element_located(note_locator))

    # Step 6: Validate note is NOT visible
    assert not notes.is_note_present(title), "Deleted note still visible in UI"



# import time
# from pages.login_page import LoginPage
# from pages.notes_page import NotesPage
# from config.environment import config

# def test_api_ui_sync_create(driver, api_client):

#     title = f"API_UI_{int(time.time())}"

#     api_client.create_note(title, "created via api")

#     login = LoginPage(driver)
#     notes = NotesPage(driver)

#     login.open(config["base_url"])
#     login.login(config["email"], config["password"])
#     login.wait_for_login_success()

#     assert notes.is_note_present(title)
