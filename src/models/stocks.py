from app import db
from datetime import datetime


class Stock(db.Model):
    __tablename__ = 'stocks'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    ticker_symbol = db.Column(db.String)
    dividends = db.relationship('Dividend', back_populates='stock', passive_deletes=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    def as_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'ticker_symbol': self.ticker_symbol,
            # TODO: dividends, etc.
        }
