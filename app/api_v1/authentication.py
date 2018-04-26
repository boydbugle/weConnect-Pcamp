from werkzeug.security import check_password_hash
from . import auth
from .views import users


@auth.verify_password
def verify_password(email, password):
    for user in users:
        if user['email'] == email:
            return check_password_hash(user.get('password'), password)
        return False