# Smart Investing App (backend)

This is the backend for Smart Investing, a web application that allows you to practice investing in the stock market.

## Setup

To install the backend, you'll first want to set up a Python 3 virtual environment, and then run:
```
pip install -r requirements.txt
```

You'll also need to set up a PostgresQL database for your app to connect to. If you have Postgres installed, simply run:
```
createdb sm_backend
```

Next you have to run migrations and seeds with:
```
flask db upgrade && flask seed
```

Now to start the app, just run
```
python app.py
```
and you're ready to go! Visit [http://localhost:5000/stocks/1](localhost:5000/stocks/1) to test out one of the endpoints and see if it's working.
