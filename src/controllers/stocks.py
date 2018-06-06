from flask import Blueprint, jsonify
from src.models.stocks import Stock

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
