import allure
from api.api_client import APIClient
import json

@allure.feature("Notes API")
def test_get_all_notes():

    api = APIClient()
    api.login()

    response = api.get_notes()
    assert response.status_code == 200

    notes = response.json().get("data", [])
    
    for i, note in enumerate(notes, 1):
        # print(f"\nNote {i}:")
        # print(json.dumps(note, indent=4))
        allure.attach(
            f"{note}",
            name=f"Note {i}",
            attachment_type=allure.attachment_type.TEXT
        )
