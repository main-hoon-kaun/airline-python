from models.wallet_model import Wallet
from .user_service import User
from database import db
from decimal import Decimal

def create_wallet(data):
    user_id = data.get('user_id')
    if user_id is None:
        raise ValueError("User ID is required")

    balance_str = data.get('balance', '0.00')
    try:
        balance = Decimal(balance_str)
    except Exception:
        raise ValueError("Invalid balance amount")

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
    if not user_id:
        raise ValueError("User ID is required")

    wallet = Wallet.query.filter_by(user_id=user_id).first()
    if not wallet:
        raise ValueError("Wallet not found")
    return wallet

def update_wallet(data):
    user_id = data.get('user_id') or data.get('userId')
    if user_id is None:
        raise ValueError("User ID is required")

    balance_str = data.get('balance')
    if balance_str is None:
        raise ValueError("New balance is required")

    try:
        new_balance = Decimal(balance_str)
    except Exception:
        raise ValueError("Invalid balance format")

    wallet = Wallet.query.filter_by(user_id=user_id).first()
    if not wallet:
        raise ValueError("Wallet not found")

    wallet.balance = new_balance
    db.session.commit()
    return wallet
