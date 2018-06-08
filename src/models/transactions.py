from app import db
from datetime import datetime
import enum


class TransactionType(enum.Enum):
    buy = 1
    sell = 2
    dividend = 3


class Transaction(db.Model):
    __tablename__ = 'transactions'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    quantity = db.Column(db.Integer)
    price = db.Column(db.Float)
    type = db.Column(db.Enum(TransactionType))

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', back_populates='transactions')

    stock_id = db.Column(db.Integer, db.ForeignKey('stocks.id'))
    stock = db.relationship('Stock')

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow, default=datetime.utcnow)

    def as_dict(self):
        return {
            'id': self.id,
            'quantity': self.quantity,
            'price': self.price,
            'type': self.type.name,
            'user_id': self.user_id,
            'stock_id': self.stock_id,
            'created_at': self.created_at.isoformat()
        }
