import unittest
import json
from base64 import b64encode
from app import create_app
from app.api_v1.user import User
from app.api_v1.authentication import verify_password


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

    def test_user_registration(self, email="app@test.com", password="app1541test", path='/api/v1/register'):
        # test successful registration
        res = self.get_agent_request(email, password, path)
        result = json.loads(res.data.decode())
        self.assertEqual(result['message'], 'successfully created user')
        self.assertEqual(res.status_code, 201)

        # test valid email
        res = self.get_agent_request('apptest', password, path)
        result = json.loads(res.data.decode())
        self.assertEqual(result['message'], 'invalid email')
        self.assertEqual(res.status_code, 403)

        # test blank email
        res = self.get_agent_request('', password, path)
        result = json.loads(res.data.decode())
        self.assertEqual(result['message'], 'invalid email')
        self.assertEqual(res.status_code, 403)

        # test valid password
        res = self.get_agent_request(email, password, path)
        result = json.loads(res.data.decode())
        self.assertEqual(result['message'], 'successfully created user')
        self.assertEqual(res.status_code, 201)

        # test invalid password
        res = self.get_agent_request(email, '48d@j', path)
        result = json.loads(res.data.decode())
        self.assertEqual(result['message'], 'invalid password')
        self.assertEqual(result['hint'], 'password atleast 8 characters of numbers/letters/special char')
        self.assertEqual(res.status_code, 403)

        # test blank password
        res = self.get_agent_request(email, '', path)
        result = json.loads(res.data.decode())
        self.assertEqual(result['message'], 'invalid password')
        self.assertEqual(res.status_code, 403)

        # test registration has no get request
        user_data = {'email': email, 'password': password}
        res = self.client().get(
            path,
            headers=self.get_api_headers(),
            data=json.dumps(user_data)
        )
        result = json.loads(res.data.decode())
        self.assertEqual(result['message'], 'invalid request')
        self.assertEqual(result['hint'], 'make a post request')
        self.assertEqual(res.status_code, 404)

        # test duplicate registration
        # res = self.get_agent_request(email, password, path)
        # res2 = self.get_agent_request(email, password, path)
        # result = json.loads(res2.data.decode())
        # self.assertEqual(result['error'], 'user in existence')
        # self.assertEqual(res2.status_code, 406)

    def test_password(self):
        # test password setter
        u = User(email='app@test.com', password='appytesty')
        self.assertTrue(u.pw_hash is not None)

        # # test password verification
        # u = User(email='app@test.com', password='appytesty')
        # u.set_password('appytesty')
        # self.assertTrue(u.check_password('appytesty'))
        # self.assertFalse(u.check_password('apptest'))

        #test password verification
        self.get_agent_request('app@test.com', 'appytesty', '/api/v1/register')
        self.assertTrue(verify_password('app@test.com', 'appytesty'))

        # test password salts are random
        u = User(email='app@test.com', password='appytesty')
        u.set_password('appytesty')
        u2 = User(email='app@test.com', password='appytesty')
        u2.set_password('appytesty')
        self.assertTrue(u.pw_hash != u2.pw_hash)

