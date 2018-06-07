from flask import Blueprint, jsonify, request
from src.models.users import User
from src.utils.auth import encode_auth_token

login_controller = Blueprint('login_controller', __name__)


@login_controller.route('/login', methods=['POST'])
def login():
    request_body = request.get_json()
    email = request_body.get('email')
    user = User.query.filter(User.email == email).one()

    password = request_body.get('password')

    if user.check_password(password):
        access_token = encode_auth_token(user.id)
        return jsonify({
            'auth': {'access_token': access_token.decode()},
            'user': user.as_dict()
        })
    else:       
        return jsonify({'error': 'Password was incorrect'}), 403
