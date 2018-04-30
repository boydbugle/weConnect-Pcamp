# import json
from . import api
from .user import User
from .validation import validate_email, validate_password
from flask import request, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash

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
                u = User(email, generate_password_hash(password))
                dict_user = u.__str__()
                users.append(dict_user)
                return make_response(jsonify({'message': 'successfully created user', 'user': dict_user}), 201)
            return make_response(
                jsonify({
                    'message': 'invalid password',
                    'hint': 'password atleast 8 characters of numbers/letters/special char'}),
                403)
        else:
            return make_response(jsonify({'message': 'invalid email'}), 403)
    return make_response(jsonify({'message': 'invalid request', 'hint': 'make a post request'}), 404)


@api.route('/login', methods=['GET', 'POST'])
def login():
    """ This route logs in a registered user """
    if request.method == 'POST':
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        user_list = {user['email']: user['password'] for user in users}
        if email in user_list:
            if check_password_hash(user_list.get(email), password):
                token = User.generate_token(email)
                if token:
                    return make_response(jsonify(
                        {'message': 'login successful',
                         'access_token': token
                         }),
                        200)
            return make_response(jsonify({'message': 'invalid password'}), 401)
        return make_response(jsonify({'message': 'invalid email please register'}), 401)
    return make_response(jsonify({'message': 'invalid request', 'hint': 'make a post request'}), 404)


@api.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    """ This route resets password to a registered account """
    if request.method == 'POST':
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        newpassword = data.get('new_password')
        user_list = {user['email']: user['password'] for user in users}
        if email in user_list:
            if check_password_hash(user_list.get(email), password):
                if validate_password(newpassword):
                    for user in users:
                        if user['email'] == email:
                            user['password'] = generate_password_hash(newpassword)
                            if check_password_hash(user['password'], newpassword):
                                return make_response(jsonify({
                                    'message': 'successful password reset',
                                    'users': users}),
                                    201)
                return make_response(
                    jsonify({
                        'message': 'invalid password',
                        'hint': 'password atleast 8 characters of numbers/letters/special char'}),
                    403)
            return make_response(jsonify({'message': 'invalid password'}), 401)
        return make_response(jsonify({'message': 'invalid email please register'}), 401)
    return make_response(jsonify({'message': 'invalid request', 'hint': 'make a post request'}), 404)
