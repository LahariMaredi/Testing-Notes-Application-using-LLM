import allure
from api.api_client import APIClient


@allure.feature("Notes API")
@allure.story("API Login and Fetch Notes")
def test_api_notes():

    api = APIClient()

    with allure.step("Login via API"):
        res = api.login()
        assert res.status_code == 200
        allure.attach(
            str(res.json()),
            name="Login Response",
            attachment_type=allure.attachment_type.JSON
        )

    with allure.step("Fetch all notes"):
        notes = api.get_notes()
        assert notes.status_code == 200
        allure.attach(
            str(notes.json()),
            name="Get Notes Response",
            attachment_type=allure.attachment_type.JSON
        )
