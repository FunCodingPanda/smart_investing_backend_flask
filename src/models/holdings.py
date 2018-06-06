from app import db
from datetime import datetime


class Holding(db.Model):
    __tablename__ = 'holdings'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    quantity = db.Column(db.Integer)
    avg_purchase_price = db.Column(db.Float)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', back_populates='holdings')

    stock_id = db.Column(db.Integer, db.ForeignKey('stocks.id'))
    stock = db.relationship('Stock')

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
