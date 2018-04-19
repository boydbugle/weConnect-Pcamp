# import json
from . import api
from .user import User
from .validation import validate_email, validate_password
from flask import request, jsonify, make_response

users = []


@api.route('/register', methods=['GET', 'POST'])
def register_user():
    """ This route registers a new user"""
    if request.method == 'POST':
        data = request.get_json()
        email = data.get('email')
        valid_email = validate_email(email)
        password = data.get('password')
        valid_password = validate_password(password)
        if valid_email:
            if valid_password:
                dict_user = User().todict(valid_email, valid_password)
                users.append(dict_user)
                return make_response(jsonify({'message': 'successfully created user'}), 201)
            return make_response(
                jsonify({
                    'message': 'invalid password',
                    "hint": 'password atleast 8 characters of numbers/letters/special char'}),
                403)
        else:
            return make_response(jsonify({'message': 'invalid email'}), 403)
