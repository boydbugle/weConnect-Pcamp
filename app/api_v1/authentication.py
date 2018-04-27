from werkzeug.security import check_password_hash
# from . import auth
from .views import users


# @auth.verify_password
def verify_password(email, password):
    user_list = {user['email']: user['password'] for user in users}
    if email in user_list and check_password_hash(user_list.get(email), password):
        return True
    elif email in user_list and check_password_hash(user_list.get(email), password) is not True:
        return "wrong password"
    return False
    # return "unauthorized user"
