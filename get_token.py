import sys
import os
sys.path.append(os.path.dirname(__file__))

from api.api_client import APIClient

api = APIClient()
api.login()
print('API Token:', api.token)