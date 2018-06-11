from app import db


class PendingDividend(db.Model):
    __tablename__ = 'pending_dividends'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    quantity = db.Column(db.Integer)
    payable_date = db.Column(db.Date, nullable=False)
    value_per_share = db.Column(db.Float, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', back_populates='pending_dividends')

    stock_id = db.Column(db.Integer, db.ForeignKey('stocks.id'))
    stock = db.relationship('Stock')

    def as_dict(self):
        return {
            'id': self.id,
            'quantity': self.quantity,
            'value_per_share': self.value_per_share,
            'stock_id': self.stock_id,
            'payable_date': self.payable_date.isoformat(),
            'created_at': self.created_at.isoformat()
        }
