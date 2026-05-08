from api.api_client import APIClient
import time

def test_api_response_time():

    api = APIClient()
    api.login()

    start = time.time()
    response = api.get_notes()
    end = time.time()

    assert response.status_code == 200
    assert (end - start) < 3
