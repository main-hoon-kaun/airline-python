

from models.wallet_model import Wallet
from .user_service import User
from database import db
from decimal import Decimal

def create_wallet(data):
    user_id = data.get('user_id')
    balance = Decimal(data.get('balance', '0.00'))

    user = User.query.get(user_id)
    if not user:
        raise ValueError("User not found")

    if hasattr(user, 'wallet') and user.wallet:
        raise ValueError("Wallet already exists for this user")

    wallet = Wallet(balance=balance, user=user)
    db.session.add(wallet)
    db.session.commit()
    return wallet

def get_wallet_by_user_id(user_id):
    wallet = Wallet.query.filter_by(user_id=user_id).first()
    if not wallet:
        raise ValueError("Wallet not found")
    return wallet

def update_wallet(data):
    user_id = data.get('user_id')
    new_balance = Decimal(data.get('balance'))

    wallet = Wallet.query.filter_by(user_id=user_id).first()
    if not wallet:
        raise ValueError("Wallet not found")

    wallet.balance = new_balance
    db.session.commit()
    return wallet
