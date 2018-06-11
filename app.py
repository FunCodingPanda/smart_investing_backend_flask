import atexit
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_cors import CORS

import os


app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
cors = CORS(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)

import src.utils.dividends
import src.utils.seed

from src.models.holding_snapshots import HoldingSnapshot
from src.models.holdings import Holding
from src.models.pending_dividends import PendingDividend
from src.models.stocks import Stock
from src.models.transactions import Transaction, TransactionType
from src.models.users import User

from src.controllers.users import users_controller
app.register_blueprint(users_controller)

from src.controllers.stocks import stocks_controller
app.register_blueprint(stocks_controller)

from src.controllers.login import login_controller
app.register_blueprint(login_controller)


# app.run(host='0.0.0.0', port=5000, debug=True)


@app.before_first_request
def initialize():
    scheduler = BackgroundScheduler()
    scheduler.start()
    scheduler.add_job(
        func=src.utils.dividends.find_and_give_pending_dividends,
        trigger=CronTrigger(hour=16, minute=30, timezone='EST'),
        id='find_and_give_pending_dividends_job',
        name='Gives out pending dividends to eligible holders',
        replace_existing=True)
    scheduler.add_job(
        func=src.utils.dividends.pay_dividends,
        trigger=CronTrigger(hour=9, minute=0, timezone='EST'),
        id='pay_dividends_job',
        name='Pays out pending dividends that have reached the payable date',
        replace_existing=True)
    # Shut down the scheduler when exiting the app
    atexit.register(lambda: scheduler.shutdown())


if __name__ == '__main__':
    app.run()
