import unittest
import json
from app import create_app
from app.api_v1.authentication import verify_password


class AuthenticationTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client

    def get_client_request(self, email='app@test.com', password='appytesty', path='/api/v1/register'):
        user_data = {'email': email, 'password': password}
        return self.client().post(
            path,
            headers={'Content-Type': 'application/json'},
            data=json.dumps(user_data)
        )

    # def test_no_auth(self):
    #     response = self.client().get(
    #         '/api/v1/businesses',
    #         content_type='application/json'
    #     )
    #     self.assertTrue(response.status_code == 401)

    def test_user_verification(self):
        # test authorized user
        self.get_client_request()
        self.assertTrue(verify_password('app@test.com', 'appytesty'))

        # test unauthorized email
        self.get_client_request()
        # self.assertEqual(verify_password('appy@testy.com', 'appytesty'), 'unauthorized email')
        self.assertFalse(verify_password('appy@testy.com', 'appytesty'))

        # test unauthorized password
        self.get_client_request()
        self.assertEqual(verify_password('app@test.com', 'apptest'), 'wrong password')

    def test_login(self):
        # test login has no get request
        user_data = {'email': 'app@test.com', 'password': 'appytesty'}
        res = self.client().get(
            '/api/v1/login',
            content_type='application/json',
            data=json.dumps(user_data)
        )
        result = json.loads(res.data.decode())
        self.assertEqual(result['message'], 'invalid request')
        self.assertEqual(result['hint'], 'make a post request')
        self.assertEqual(res.status_code, 404)
