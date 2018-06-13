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

    def __repr__(self):
        """
        This function is used for converting a `Stock` object into a string
        representation. This is useful when writing queries in the terminal.
        """
        return "<HoldingSnapshot(id={}, user_id={}, portfolio_value={})>".format(self.id, self.user_id, self.portfolio_value)

    def as_dict(self):
        return {
            'id': self.id,
            'portfolio_value': self.portfolio_value,
            'user_id': self.user_id,
            'created_at': self.created_at.isoformat()
         }
