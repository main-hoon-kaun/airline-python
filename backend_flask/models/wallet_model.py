from database import db
from decimal import Decimal
from .user_model import User  # Adjust if User is in a different module or package

class Wallet(db.Model):
    __tablename__ = 'wallet'

    id = db.Column(db.Integer, primary_key=True)
    balance = db.Column(db.Numeric(precision=10, scale=2), nullable=True, default=Decimal('0.00'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    user = db.relationship('User', backref=db.backref('wallet', uselist=False))

    def __init__(self, balance=Decimal('0.00'), user=None):
        self.id = Wallet.get_next_id()
        self.balance = balance
        self.user = user

    @staticmethod
    def get_next_id():
        current_max = db.session.query(db.func.max(Wallet.id)).scalar()
        return (current_max or 0) + 1

    def __repr__(self):
        return f"<Wallet id={self.id} balance={self.balance} user_id={self.user_id}>"
