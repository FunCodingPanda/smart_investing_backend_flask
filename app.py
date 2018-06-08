import atexit
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import date
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_cors import CORS
import requests
import schedule 
import time 

import os


app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
cors = CORS(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
cron = BackgroundScheduler(daemon=True)

import src.utils.seed

from src.models.dividend_payouts import DividendPayout
from src.models.dividends import Dividend
from src.models.holding_snapshots import HoldingSnapshot
from src.models.holdings import Holding
from src.models.stocks import Stock
from src.models.transactions import Transaction, TransactionType
from src.models.users import User

from src.controllers.users import users_controller
app.register_blueprint(users_controller)

from src.controllers.stocks import stocks_controller
app.register_blueprint(stocks_controller)

from src.controllers.login import login_controller
app.register_blueprint(login_controller)


@app.route('/')
def hello():
    return 'Hello Panda!'

# create two functions (one with paying out dividend and calculating dividends)
# paying out dividend - credit user with quantity * dividend price
# calculate dividend  - 1st step get the holdings of all users


def payout_dividend(user_id, quantity, dividend_id):
    # 1. Credit user with quantity * dividend.price cash
    # user with dividend stocks  
    # add the dividends to the user's cash
    # send the dividends to the transaction table
    pass


def calculate_dividends():
    # 1. Get a list of all stocks held by users 
    for holding in db.session.query(Holding).filter(Holding.quantity > 0).all():
        print(holding)
        user = holding.user
        stock = holding.stock
        # 2. For each one, look up dividends on the IEX API 
        data = requests.get('https://api.iextrading.com/1.0/stock/{}/dividends/1m'.format(stock.ticker_symbol))
        for dividend in data.json():
            print(dividend)
        # 3. If there is a dividend with an "ex date" of tomorrow, then:
            # if dividend['exDate']... the external API is behind on the dividend date
        # 4. Schedule a new cron job to pay the user on the "payment date"


# <https://stackoverflow.com/questions/21214270/scheduling-a-function-to-run-every-hour-on-flask>
# cron.add_job(calculate_dividends, 'cron', hour=16, minute=30, timezone='EST')
cron.add_job(calculate_dividends, 'interval', hour=16, minute=30, timezone='EST')
cron.start()


# Shutdown your cron thread if the web process is stopped
atexit.register(lambda: cron.shutdown(wait=False))


# def job():
#     print("It is working")

# # schedule.every(1).minutes.do(job)
# # schedule.every().hour.do(job)
# schedule.every(1).seconds.do(job)
# schedule.every().day.at("16:30").do(job)
# # schedule.every().monday.do(job)
# # schedule.every().wednesday.at("13:15").do(job)

# while True:
#     schedule.run_pending()
#     time.sleep(1)

# app.run(host='0.0.0.0', port=5000, debug=True)
if __name__ == '__main__':
    app.run()
