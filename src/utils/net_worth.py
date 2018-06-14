from app import db
import requests
from src.models.holding_snapshots import HoldingSnapshot
from src.models.stocks import Stock
from src.models.users import User
from sqlalchemy.orm import subqueryload


def update_all():
    print("starting update")
    # 1. Look up all our stock tickers
    symbols_by_id = dict((s.id, s.ticker_symbol) for s in Stock.query.all())

    # 2. Look up all current stock prices
    data = requests.get('https://api.iextrading.com/1.0/tops/last')
    stock_prices = {}
    for item in data.json():
        ticker_symbol = item['symbol']
        price = item['price']
        stock_prices[ticker_symbol] = price

    # 3. Look up each user and their current holdings
    # http://docs.sqlalchemy.org/en/latest/orm/query.html
    users = User.query.options(subqueryload(User.holdings)).all()

    # 4. Calculate the value of their current holdings + their cash (ie. net worth)
    for user in users:
        net_worth = user.cash
        for holding in user.holdings:
            symbol = symbols_by_id[holding.stock_id]
            current_price = stock_prices.get(symbol, 0)
            net_worth += current_price * holding.quantity
        holding_snapshot = HoldingSnapshot(user_id=user.id,
                                           portfolio_value=net_worth)
        db.session.add(holding_snapshot)

    # 5. Write the data into the holdings snapshots table
    db.session.commit()
    print("finished update")

# symbols_by_id = {
#     1: 'MSFT',
#     2: 'AMZN',
#     3: 'TWTR'
# }

# stock_prices = {
#     'MSFT': 101.32,
#     'AMZN': 2000,
#     'TWTR': 194.23
# }
