from werkzeug.security import generate_password_hash, check_password_hash


class User:
    def __init__(self, email=None, password=None):
        self.email = email
        self.pw_hash = password
        # self.user_id = user_id

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pw_hash, password)

    @staticmethod
    def todict(email, password):
        user = {
            'email': email,
            'password': password,
            # 'user_id': user_id
        }
        return user
