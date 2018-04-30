from werkzeug.security import generate_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadData, BadSignature
from flask import current_app


class User:
    def __init__(self, email=None, password=None):
        self.email = email
        self.pw_hash = password

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)

    @staticmethod
    def generate_token(email):
        try:
            s = Serializer(current_app.config['SECRET_KEY'], expires_in=1800)
            return s.dumps({'email': email})
        except Exception as e:
            return str(e)

    @staticmethod
    def decode_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])

    def __str__(self):
        user = {
            'email': self.email,
            'password': self.pw_hash,
        }
        return user
