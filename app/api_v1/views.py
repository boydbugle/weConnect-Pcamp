# import json
from . import api
from .user import User
from flask import request, jsonify, make_response

users = []


@api.route('/register', methods=['GET', 'POST'])
def register_user():
    """ This route registers a new user"""
    if request.method == 'POST':
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        create_user = User(email, password)
        users.append(create_user)
        return make_response(jsonify({'message': 'successfully created user'}), 201)
