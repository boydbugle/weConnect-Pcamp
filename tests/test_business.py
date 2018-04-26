import unittest
import json
from base64 import b64encode
from app import create_app
# from app.api_v1.user import User


class UserTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client

    @staticmethod
    def get_api_headers(email='', password=''):
        return {
            'Authorization':
                'Basic' + b64encode((email + ':' + password).encode('utf-8')).decode('utf-8'),
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

    def get_agent_request(self, email=None, password=None, path=None):
        user_data = {'email': email, 'password': password}
        return self.client().post(
            path,
            headers=self.get_api_headers(),
            data=json.dumps(user_data)
        )

    def test_no_auth(self):
        response = self.client().get(
            'api/v1/businesses',
            headers=self.get_api_headers()
        )
        self.assertTrue(response.status_code == 401)