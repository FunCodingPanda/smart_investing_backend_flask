from app import db
from flask import Blueprint, jsonify, request
import re
# from flask import Flask, request
# from flask_sqlalchemy import SQLAlchemy
# import uuid
# from werkzeug.security import generate_password_hash, check_hash

from src.models.users import User
from src.utils.auth import encode_auth_token

# app.config['SECRET_KEY'] = 'thisissecret'
# app.config['SQLALCHEMY_DATABSE_URI'] = 'sqlity////mnt/c/Users/autho/Documents/api_example/todo.db'

users_controller = Blueprint('users_controller', __name__)
EMAIL_REGEX = r'^\w+[-\w\.]*\@\w+((-\w+)|(\w*))\.[a-z]{2,3}$'


@users_controller.route('/users', methods=['GET'])
def get_all_users():
    users = User.query.all()
    user_dicts = [user.as_dict() for user in users]
    return jsonify(user_dicts)


@users_controller.route('/users/<int:user_id>')
def get_one_user(user_id):
    user = User.query.filter(User.id == user_id).one()
    return jsonify(user.as_dict())


@users_controller.route('/users', methods=['POST'])
def create_user():
    request_body = request.get_json()
    print(request_body)
    if request_body.get('name') is None:
        return jsonify({'error': 'Name is required'}), 400
    elif len(request_body['name']) < 4:
        return jsonify({'error': 'Name should be at least 4 characters'}), 400
    elif request_body.get('email') is None:
        return jsonify({'error': 'Email is required'}), 400
    elif not re.match(EMAIL_REGEX, request_body['email']):
        return jsonify({'error': 'Email is invalid'}), 400
    elif request_body.get('password') is None:
        return jsonify({'error': 'Password is required'}), 400
    elif request_body.get('password') != request_body.get('confirmPassword'):
        return jsonify({'error': 'Passwords do not match'}), 400

    user = User(name=request_body['name'],
                email=request_body['email'],
                password=request_body['password'],
                cash=20000.0)
    db.session.add(user)
    db.session.commit()

    auth_token = encode_auth_token(user.id)

    return jsonify({
        'user': user.as_dict(),
        'auth': {
            'access_token': auth_token.decode()
        }
    }), 201
