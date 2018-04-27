from werkzeug.security import generate_password_hash


class User:
    def __init__(self, email=None, password=None):
        self.email = email
        self.pw_hash = password

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)

    def __str__(self):
        user = {
            'email': self.email,
            'password': self.pw_hash,
        }
        return user
