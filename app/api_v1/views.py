# import json
from . import api
from .user import User
from .validation import validate_email
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
        if valid_email:
            dict_user = User().todict(valid_email, password)
            users.append(dict_user)
            return make_response(jsonify({'message': 'successfully created user'}), 201)
        else:
            return make_response(jsonify({'message': 'invalid email'}), 403)

