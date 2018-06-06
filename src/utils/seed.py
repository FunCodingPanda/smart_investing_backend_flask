from app import app, db
import requests
from src.models.stocks import Stock
from src.models.users import User


@app.cli.command()
def seed():
    """Perform database seeding."""

    #
    # Run users seeds
    #
    user = User(email="test@test.com",
                name='Tom',
                password='testp@ssw0rd',
                cash=20000.00)
    # Add a query to insert this user into the DB
    db.session.add(user)

    #
    # Run stocks seeds
    #
    data = requests.get('https://api.iextrading.com/1.0/ref-data/symbols')
    for item in data.json():
        stock = Stock(name=item['name'], ticker_symbol=item['symbol'])
        db.session.add(stock)

    # Now finally run the query
    db.session.commit()
    print('Finished running seeds!')
