class User:
    def __init__(self, email=None, password=None):
        self.email = email
        self.password = password
        # self.user_id = user_id

    def todict(self, email, password):
        user = {
            'email': email,
            'password': password,
            # 'user_id': user_id
        }
        return user
