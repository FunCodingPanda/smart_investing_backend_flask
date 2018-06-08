from app import db


class DividendPayout(db.Model):
    __tablename__ = 'dividend_payouts'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    quantity = db.Column(db.Integer)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', back_populates='dividend_payouts')

    dividend_id = db.Column(db.Integer, db.ForeignKey('dividends.id'))
    dividend = db.relationship('Dividend')

    def as_dict(self):
        return {
            'id': self.id,
            'quantity': self.quantity,
            'dividend_id': self.dividend_id,
            'created_at': self.created_at.isoformat()
        }