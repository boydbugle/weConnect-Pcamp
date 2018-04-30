import unittest
import json
from base64 import b64encode
from app import create_app
from app.api_v1.user import User


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

    def get_client_request(self, email='app@test.com', password='appytesty', path='/api/v1/register'):
        user_data = {'email': email, 'password': password}
        return self.client().post(
            path,
            headers=self.get_api_headers(),
            data=json.dumps(user_data)
        )

    def test_user_registration(self):
        # test successful registration
        res = self.get_client_request()
        result = json.loads(res.data.decode())
        self.assertEqual(result['message'], 'successfully created user')
        self.assertEqual(res.status_code, 201)

        # test valid email
        res = self.get_client_request(email='apptest')
        result = json.loads(res.data.decode())
        self.assertEqual(result['message'], 'invalid email')
        self.assertEqual(res.status_code, 403)

        # test blank email
        res = self.get_client_request(email='')
        result = json.loads(res.data.decode())
        self.assertEqual(result['message'], 'invalid email')
        self.assertEqual(res.status_code, 403)

        # test valid password
        res = self.get_client_request()
        result = json.loads(res.data.decode())
        self.assertEqual(result['message'], 'successfully created user')
        self.assertEqual(res.status_code, 201)

        # test invalid password
        res = self.get_client_request(password='48d@j')
        result = json.loads(res.data.decode())
        self.assertEqual(result['message'], 'invalid password')
        self.assertEqual(result['hint'], 'password atleast 8 characters of numbers/letters/special char')
        self.assertEqual(res.status_code, 403)

        # test blank password
        res = self.get_client_request(password='')
        result = json.loads(res.data.decode())
        self.assertEqual(result['message'], 'invalid password')
        self.assertEqual(res.status_code, 403)

        # test registration has no get request
        user_data = {'email': 'app@test.com', 'password': 'appytesty'}
        res = self.client().get(
            '/api/v1/register',
            headers=self.get_api_headers(),
            data=json.dumps(user_data)
        )
        result = json.loads(res.data.decode())
        self.assertEqual(result['message'], 'invalid request')
        self.assertEqual(result['hint'], 'make a post request')
        self.assertEqual(res.status_code, 404)

        # test duplicate registration
        # self.get_client_request(email, password, path)
        # res2 = self.get_client_request(email, password, path)
        # result = json.loads(res2.data.decode())
        # self.assertEqual(result['error'], 'user in existence')
        # self.assertEqual(res2.status_code, 406)

    def test_password(self):
        # test password setter
        u = User(email='app@test.com', password='appytesty')
        self.assertTrue(u.pw_hash is not None)

        # test password salts are random
        u = User(email='app@test.com', password='appytesty')
        u.set_password('appytesty')
        u2 = User(email='app@test.com', password='appytesty')
        u2.set_password('appytesty')
        self.assertTrue(u.pw_hash != u2.pw_hash)

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

        # test successful login and token generated
        self.get_client_request()
        res = self.get_client_request(path='/api/v1/login')
        result = json.loads(res.data.decode())
        self.assertEqual(result['message'], "login successful")
        self.assertTrue(result['access_token'])
        self.assertEqual(res.status_code, 200)

        # test unauthorized email
        self.get_client_request()
        res = self.get_client_request(email='appy@testy.com', path='/api/v1/login')
        result = json.loads(res.data.decode())
        self.assertEqual(result['message'], "invalid email please register")
        self.assertEqual(res.status_code, 401)

        # test invalid password
        self.get_client_request()
        res = self.get_client_request(password='apptest', path='/api/v1/login')
        result = json.loads(res.data.decode())
        self.assertEqual(result['message'], "invalid password")
        self.assertEqual(res.status_code, 401)

        # test token is  generated
    def test_reset_password(self):
        # test reset_password has no get request
        user_data = {'email': 'app@test.com', 'password': 'appytesty'}
        res = self.client().get(
            '/api/v1/reset_password',
            content_type='application/json',
            data=json.dumps(user_data)
        )
        result = json.loads(res.data.decode())
        self.assertEqual(result['message'], 'invalid request')
        self.assertEqual(result['hint'], 'make a post request')
        self.assertEqual(res.status_code, 404)

        # test unauthorized user
        self.get_client_request()
        res = self.get_client_request(email='appy@testy.com', path='/api/v1/reset_password')
        result = json.loads(res.data.decode())
        self.assertEqual(result['message'], "invalid email please register")
        self.assertEqual(res.status_code, 401)

        # test incorrect password
        self.get_client_request()
        res = self.get_client_request(password='apptest', path='/api/v1/reset_password')
        result = json.loads(res.data.decode())
        self.assertEqual(result['message'], "invalid password")
        self.assertEqual(res.status_code, 401)

        # test validity of new password
        self.get_client_request()
        user_data = {'email': 'app@test.com', 'password': 'appytesty', 'new_password': 'cdsb5'}
        res = self.client().post(
            '/api/v1/reset_password',
            content_type='application/json',
            data=json.dumps(user_data)
        )
        result = json.loads(res.data.decode())
        self.assertEqual(result['message'], 'invalid password')
        self.assertEqual(result['hint'], 'password atleast 8 characters of numbers/letters/special char')
        self.assertEqual(res.status_code, 403)

        # test successful password reset
        self.get_client_request()
        user_data = {'email': 'app@test.com', 'password': 'appytesty', 'new_password': 'resetpass'}
        res = self.client().post(
            '/api/v1/reset_password',
            content_type='application/json',
            data=json.dumps(user_data)
        )
        result = json.loads(res.data.decode())
        self.assertEqual(result['message'], "successful password reset")
        self.assertEqual(res.status_code, 201)
