from app import db
from datetime import datetime


class Stock(db.Model):
    __tablename__ = 'stocks'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    ticker_symbol = db.Column(db.String)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    def __repr__(self):
        """
        This function is used for converting a `Stock` object into a string
        representation. This is useful when writing queries in the terminal.
        """
        return "<Stock(id={}, ticker_symbol={})>".format(self.id, self.ticker_symbol)

    def as_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'ticker_symbol': self.ticker_symbol
        }
