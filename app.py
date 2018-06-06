from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import os


app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)

import src.utils.seed

from src.models.dividend_payouts import DividendPayout
from src.models.dividends import Dividend
from src.models.holding_snapshots import HoldingSnapshot
from src.models.holdings import Holding
from src.models.stocks import Stock
from src.models.transactions import Transaction
from src.models.users import User

from src.controllers.users import users_controller
app.register_blueprint(users_controller)

from src.controllers.stocks import stocks_controller
app.register_blueprint(stocks_controller)

from src.controllers.login import login_controller
app.register_blueprint(login_controller)


@app.route('/')
def hello():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
