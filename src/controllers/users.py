from app import db
from flask import Blueprint, jsonify, request
import re
# from flask import Flask, request
# from flask_sqlalchemy import SQLAlchemy
# import uuid
# from werkzeug.security import generate_password_hash, check_hash

from src.models.users import User
from src.models.stocks import Stock
from src.models.holdings import Holding
from src.models.holding_snapshots import HoldingSnapshot
from src.models.transactions import Transaction
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


@users_controller.route('/users/<int:user_id>/holdings', methods=['GET'])
def get_user_holdings(user_id):
    holdings = []
    for holding, stock in db.session.query(Holding, Stock) \
                                    .filter(Holding.stock_id == Stock.id) \
                                    .filter(Holding.user_id == user_id) \
                                    .filter(Holding.quantity > 0) \
                                    .all():
        holdings.append({
            'quantity': holding.quantity,
            'avg_purchase_price': holding.avg_purchase_price,
            'ticker_symbol': stock.ticker_symbol,
            'name': stock.name
        })
    return jsonify(holdings)

# JavaScript:
# return knex('holdings')
#   .join('stocks', 'stocks.id', 'holdings.stock_id')
#   .select('holdings.quantity', 'stocks.ticker_symbol', 'stocks.name')
#   .where('holdings.user_id', '=', user_id)
#   .andWhere('quantity', '>', 0); // only select holdings with quantity > 0


@users_controller.route('/users/<int:user_id>/transactions', methods=['GET'])
def get_user_transactions(user_id):
    transactions = []
    for transaction, stock in db.session.query(Transaction, Stock) \
                                        .filter(Transaction.stock_id == Stock.id)\
                                        .filter(Transaction.user_id == user_id) \
                                        .order_by(Transaction.created_at.desc()) \
                                        .all():
        transactions.append({
            'quantity': transaction.quantity,
            'price': transaction.price,
            'total': transaction.quantity * transaction.price,
            'ticker_symbol': stock.ticker_symbol,
            'name': stock.name,
            'created_at': transaction.created_at,
            'type': transaction.type.name
        })
    return jsonify(transactions)


@users_controller.route('/users/<int:user_id>/holding_snapshots', methods=['GET'])
def get_user_holding_snapshots(user_id):
    snapshots = []
    for snapshot in HoldingSnapshot.query \
                                   .filter(HoldingSnapshot.user_id == user_id) \
                                   .order_by(HoldingSnapshot.created_at.asc()).all():
        timestamp = int(snapshot.created_at.timestamp() * 1000)
        snapshots.append([timestamp, snapshot.portfolio_value])
    return jsonify(snapshots)


# return knex('transactions')
#     .join('stocks', 'stocks.id', 'transactions.stock_id')
#     .select(
#       'quantity',
#       'price',
#       'total',
#       'ticker_symbol',
#       'name',
#       'transactions.created_at',
#       'type')
#     .where('transactions.user_id', '=', user_id)
#     .orderBy('created_at', 'desc')
