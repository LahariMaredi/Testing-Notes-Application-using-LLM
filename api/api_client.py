import requests
from config.environment import config
from api.endpoints import *

class APIClient:

    def __init__(self):
        self.base_url = config["api_url"]
        self.token = None

    def login(self):
        url = self.base_url + LOGIN
        payload = {
            "email": config["email"],
            "password": config["password"]
        }
        res = requests.post(url, json=payload)
        assert res.status_code == 200, f"Login failed: {res.status_code} {res.text}"
        response_json = res.json()
        self.token = response_json.get("data", {}).get("token")
        assert self.token, f"Missing token in login response: {res.text}"
        return res

    def headers(self):
        return {"x-auth-token": self.token}

    def get_notes(self):
        return requests.get(self.base_url + GET_NOTES, headers=self.headers())

    def create_note(self, title, desc, category="Home"):
        payload = {"title": title, "description": desc, "category": category}
        return requests.post(self.base_url + CREATE_NOTE, json=payload, headers=self.headers())

    def delete_note(self, note_id):
        url = self.base_url + f"/notes/{note_id}"
        return requests.delete(url, headers=self.headers())
