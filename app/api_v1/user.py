from werkzeug.security import generate_password_hash, check_password_hash


class User:
    def __init__(self, email=None, password=None):
        self.email = email
        self.pw_hash = password
        # self.user_id = user_id

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        # print(self.pw_hash)
        
    def check_password(self, password):
        return check_password_hash(self.pw_hash, password)

    def __str__(self):
        user = {
            'email': self.email,
            'password': self.pw_hash,
            # 'user_id': user_id
        }
        return user
