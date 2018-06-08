from app import db
from datetime import datetime


class Dividend(db.Model):
    __tablename__ = 'dividends'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    amount_per_share = db.Column(db.Float)
    payable_date = db.Column(db.DateTime, nullable=False)
    stock_id = db.Column(db.Integer, db.ForeignKey('stocks.id'))
    stock = db.relationship('Stock', back_populates='dividends')
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    def as_dict(self):
        return {
            'id': self.id,
            'amount_per_share': self.amount_per_share,
            'payable_date': self.payable_date.isoformat(),
            'stock_id': self.stock_id,
            'created_at': self.created_at.isoformat()
        }
