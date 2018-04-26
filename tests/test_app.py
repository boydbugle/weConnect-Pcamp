import unittest
from flask import current_app
from app import create_app


class AppTESTCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client

    def tearDown(self):
        self.app_context.pop()

    def test_app_exists(self):
        self.assertFalse(current_app is None)

    def test_app_is_testing(self):
        self.assertTrue(current_app.config['TESTING'])

    def test_no_auth(self):
        response = self.client().get(
            'api/v1/businesses',
            content_type='application/json'
        )
        self.assertTrue(response.status_code == 401)