from app import db
from datetime import datetime


class HoldingSnapshot(db.Model):
    __tablename__ = 'holding_snapshots'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    portfolio_value = db.Column(db.Float)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', back_populates='holding_snapshots')

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    def as_dict(self):
        return {
            'id': self.id,
            'portfolio_value': self.portfolio_value,
            'user_id': self.user_id,
            'created_at': self.created_at.isoformat()
         }
