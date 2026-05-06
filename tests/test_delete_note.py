import time
import allure
from api.api_client import APIClient


@allure.feature("Notes API")
@allure.story("Delete Note")
def test_delete_note_api():

    api = APIClient()
    
    with allure.step("Login to API"):
        api.login()

    title = f"API_DEL_{int(time.time())}"

    with allure.step(f"Create note with title: {title}"):
        create = api.create_note(title, "delete test")
        assert create.status_code in [200, 201]
        allure.attach(
            str(create.json()),
            name="Create Note Response",
            attachment_type=allure.attachment_type.JSON
        )

    with allure.step("Extract note ID from response"):
        note_id = create.json()["data"]["id"]
        allure.attach(f"Note ID: {note_id}", name="Note ID", attachment_type=allure.attachment_type.TEXT)

    with allure.step(f"Delete note with ID: {note_id}"):
        delete = api.delete_note(note_id)
        assert delete.status_code == 200
        allure.attach(
            str(delete.json()),
            name="Delete Note Response",
            attachment_type=allure.attachment_type.JSON
        )
