import unittest
import json
from base64 import b64encode
from app import create_app


class UserTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client

    def get_api_headers(self, email='', password=''):
        return {
            'Authorizarion':
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

    def test_user_can_register_successfully(self, email="app@test.com", password="app1541test"):
        res = self.get_agent_request(email, password, '/api/v1/register')
        result = json.loads(res.data.decode())
        self.assertEqual(result['message'], 'successfully created user')
        self.assertEqual(res.status_code, 201)

    def test_user_email_validation(self, email="apptest.cm", password="apptest"):
        res = self.get_agent_request(email, password, '/api/v1/register')
        result = json.loads(res.data.decode())
        self.assertEqual(result['message'], 'invalid email')
        self.assertEqual(res.status_code, 403)

    def test_blank_email(self, email='', password='apptest'):
        res = self.get_agent_request(email, password, '/api/v1/register')
        result = json.loads(res.data.decode())
        self.assertEqual(result['message'], 'invalid email')
        self.assertEqual(res.status_code, 403)

    def test_valid_password(self, email='app@test.com', password='appytesty'):
        res = self.get_agent_request(email, password, '/api/v1/register')
        result = json.loads(res.data.decode())
        self.assertEqual(result['message'], 'successfully created user')
        self.assertEqual(res.status_code, 201)

    def test_invalid_password(self, email='app@test.com', password='48d@j'):
        res = self.get_agent_request(email, password, '/api/v1/register')
        result = json.loads(res.data.decode())
        self.assertEqual(result['message'], 'invalid password')
        self.assertEqual(result['hint'], 'password atleast 8 characters of numbers/letters/special char')
        self.assertEqual(res.status_code, 403)

    def test_blank_password(self, email='app@test.com', password=''):
        res = self.get_agent_request(email, password, '/api/v1/register')
        result = json.loads(res.data.decode())
        self.assertEqual(result['message'], 'invalid password')
        self.assertEqual(res.status_code, 403)
