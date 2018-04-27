import unittest
import json
from app import create_app
from app.api_v1.authentication import verify_password


class AuthenticationTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client

    def test_no_auth(self):
        response = self.client().get(
            '/api/v1/businesses',
            content_type='application/json'
        )
        self.assertTrue(response.status_code == 401)

    def test_user_verification(self, email='app@test.com', password='appytesty'):
        # test authorized user
        user_data ={'email': email, 'password': password}
        self.client().post(
            '/api/v1/register',
            content_type='application/json',
            data=json.dumps(user_data)
        )
        self.assertTrue(verify_password('app@test.com', 'appytesty'))

        # test unauthorized email
        user_data = {'email': email, 'password': password}
        self.client().post(
            '/api/v1/register',
            content_type='application/json',
            data=json.dumps(user_data)
        )
        # self.assertEqual(verify_password('appy@testy.com', 'appytesty'), 'unauthorized email')
        self.assertFalse(verify_password('appy@testy.com', 'appytesty'))

        # test unauthorized password
        user_data = {'email': email, 'password': password}
        self.client().post(
            '/api/v1/register',
            content_type='application/json',
            data=json.dumps(user_data)
        )
        self.assertEqual(verify_password('app@test.com', 'apptest'), 'wrong password')
