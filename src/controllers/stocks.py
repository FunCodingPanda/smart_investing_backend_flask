from app import db
from flask import Blueprint, jsonify, request
from src.models.holdings import Holding
from src.models.stocks import Stock
from src.models.transactions import Transaction, TransactionType
from src.models.users import User

stocks_controller = Blueprint('stock_controller', __name__)


@stocks_controller.route('/stocks')
def get_all_stocks():
    stocks = Stock.query.all()
    stock_dicts = [stock.as_dict() for stock in stocks]
    return jsonify(stock_dicts)


@stocks_controller.route('/stocks/<int:stock_id>')
def get_one_stock(stock_id):
    stock = Stock.query.filter(Stock.id == stock_id).one()
    return jsonify(stock.as_dict())


@stocks_controller.route('/stocks/<string:ticker_symbol>/buy', methods=['POST'])
def buy_stock(ticker_symbol):
    # Parse the request body parameters
    request_body = request.get_json()
    quantity = int(request_body['quantity'])
    price = float(request_body['price'])
    user_id = int(request_body['userId'])

    if quantity <= 0:
        return jsonify({'error': 'Cannot buy zero or less'}), 400

    # Check that the stock exists
    stock = Stock.query.filter(Stock.ticker_symbol == ticker_symbol).first()
    if stock is None:
        return jsonify({'error': 'Stock not found'}), 404

    # Check that the user exists and that they have enough cash
    user = User.query.filter(User.id == user_id).first()
    if user is None:
        return jsonify({'error': 'User not found'}), 404
    elif user.cash < quantity * price:
        return jsonify({'error': 'User does not have enough cash'}), 400

    # Decrement user's cash
    user.cash -= quantity * price

    # Add or create a holding for this stock/user combo
    holding = Holding.query.filter(Holding.stock_id == stock.id) \
                           .filter(Holding.user_id == user_id) \
                           .first()
    if holding is None:
        holding = Holding(stock=stock, user=user, quantity=quantity,
                          avg_purchase_price=price)
    else:
        old_total = holding.avg_purchase_price * holding.quantity
        new_total = price * quantity
        holding.quantity += quantity
        holding.avg_purchase_price = (old_total + new_total) / holding.quantity

    # Create a transaction
    transaction = Transaction(type=TransactionType.buy, user=user, stock=stock,
                              quantity=quantity, price=price)

    # Commit all the changes to the DB
    db.session.add(user)
    db.session.add(holding)
    db.session.add(transaction)
    db.session.commit()

    return jsonify({
        'transaction': transaction.as_dict(),
        'cash': user.cash,
        'holding': holding.as_dict()
    })


@stocks_controller.route('/stocks/<string:ticker_symbol>/sell', methods=['POST'])
def sell_stock(ticker_symbol):
    # Parse the request body parameters
    request_body = request.get_json()
    quantity = int(request_body['quantity'])
    price = float(request_body['price'])
    user_id = int(request_body['userId'])

    if quantity <= 0:
        return jsonify({'error': 'Cannot sell zero or less'}), 400

    # Check that the stock exists
    stock = Stock.query.filter(Stock.ticker_symbol == ticker_symbol).first()
    if stock is None:
        return jsonify({'error': 'Stock not found'}), 404

    # 2. Check that the user exists and has enough of the STOCK
    holding = Holding.query.filter(Holding.stock_id == stock.id) \
                           .filter(Holding.user_id == user_id) \
                           .first()
    if holding is None or holding.quantity < quantity:
        return jsonify({'error': 'User does not have enough of this stock'}), 400

    # 3. Increase the user's cash
    user = User.query.filter(User.id == user_id).first()
    if user is None:
        return jsonify({'error': 'User not found'}), 404

    user.cash += price * quantity

    # 4. Decrease the user's holding
    holding.quantity -= quantity

    # 5. Create a transaction
    transaction = Transaction(type=TransactionType.sell, user=user, stock=stock,
                              quantity=quantity, price=price)
    # 6. Commit all the changes to the DB
    db.session.add(user)
    db.session.add(holding)
    db.session.add(transaction)
    db.session.commit()

    return jsonify({
        'transaction': transaction.as_dict(),
        'cash': user.cash,
        'holding': holding.as_dict()
    })
