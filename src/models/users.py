from app import bcrypt, db
from datetime import datetime


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String, unique=True)
    name = db.Column(db.String)
    hashed_password = db.Column(db.String)
    cash = db.Column(db.Float)
    pending_dividends = db.relationship('PendingDividend', back_populates='user', passive_deletes=True)
    holdings = db.relationship('Holding', back_populates='user', passive_deletes=True)
    holding_snapshots = db.relationship('HoldingSnapshot', back_populates='user', passive_deletes=True)
    transactions = db.relationship('Transaction', back_populates='user', passive_deletes=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    # constructor
    def __init__(self, name, email, password, cash=20000.00):
        self.name = name
        self.email = email
        self.cash = cash
        self.hashed_password = bcrypt.generate_password_hash(password).decode()

    def as_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'name': self.name,
            'cash': self.cash
        }

    def check_password(self, password):
        return bcrypt.check_password_hash(self.hashed_password, password)


# Example:
# sophie = User('Sophie', 'sophie@panda.com', 'boogers')
# sophie.as_dict()
# {
#     'id': 3,
#     'email': 'sophie@panda.com',
#     'name': 'Sophie',
#     'cash': 20000.00
# }
# sophie.check_password('panda')
