from app import db
import datetime
import pandas_market_calendars as mcal
import requests

from src.models.holdings import Holding
from src.models.pending_dividends import PendingDividend
from src.models.stocks import Stock
from src.models.transactions import Transaction, TransactionType
from src.models.users import User


def get_next_market_day():
    nyse = mcal.get_calendar('NYSE')
    today = datetime.date.today()
    tomorrow = today + datetime.timedelta(days=1)
    tomorrow_plus_week = tomorrow + datetime.timedelta(days=7)
    market_dates = nyse.schedule(start_date=tomorrow.isoformat(),
                                 end_date=tomorrow_plus_week.isoformat())
    return market_dates.iloc[0].name.date()


# https://github.com/rsheftel/pandas_market_calendars
def get_dividends_by_ex_date(ex_date):
    params = {
        'country': 'us',
        'getDividends': 'true',
        'fields': 'symbol,amount,exDivDate,payableDate',
        'page': 1,
        'limit': 1000,
        'startDate': ex_date.isoformat()
    }
    data = requests.get('https://core-api.barchart.com/v1/earnings-dividends/get', params=params)
    return data.json().get('data', [])


def find_and_give_pending_dividends():
    # 1. Look up the latest dividend info from the Barchart API
    next_market_day = get_next_market_day()
    dividends = get_dividends_by_ex_date(next_market_day)
    symbols_with_ex_date_next_market_day = list(map(lambda d: d['symbol'], dividends))
    # 2. Find all the stocks in the DB that have holdings
    holdings = Holding.query \
                      .join(Stock) \
                      .filter(Stock.ticker_symbol.in_(symbols_with_ex_date_next_market_day)) \
                      .all()
    # 3. Give pending dividends to all holders of those stocks
    for holding in holdings:
        dividend = list(filter(lambda d: d['symbol'] == holding.stock.ticker_symbol, dividends))[0]
        payable_date = datetime.datetime.strptime(dividend['payableDate'], '%m/%d/%y').date()
        value_per_share = float(dividend['amount'].strip('$'))
        pending_dividend = PendingDividend(user_id=holding.user_id,
                                           stock_id=holding.stock_id,
                                           quantity=holding.quantity,
                                           payable_date=payable_date,
                                           value_per_share=value_per_share)
        db.session.add(pending_dividend)
    db.session.commit()


def pay_dividends():
    # 1. Find all pending dividends with today as the payable date
    today = datetime.date.today()
    pending_dividends = PendingDividend.query.filter(PendingDividend.payable_date == today)
    # 2. Credit the respective users with their dividends
    for pending_dividend in pending_dividends:
        user = User.query.filter(User.id == pending_dividend.user_id).one()
        user.cash += pending_dividend.value_per_share * pending_dividend.quantity
        db.session.add(user)
        # 3. Record a transaction for each payment
        transaction = Transaction(quantity=pending_dividend.quantity,
                                  price=pending_dividend.value_per_share,
                                  type=TransactionType.dividend,
                                  user_id=pending_dividend.user_id,
                                  stock_id=pending_dividend.stock_id)
        db.session.add(transaction)
        # 4. Delete the pending dividend
        db.session.delete(pending_dividend)
        db.session.commit()
