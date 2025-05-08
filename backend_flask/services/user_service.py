from models.user_model import User
from database import db

def create_user(username, email, password, role='CUSTOMER'):
    user = User(username=username, email=email, password=password, role=role)
    db.session.add(user)
    db.session.commit()
    return user

def authenticate_user(email, password):
    user = User.query.filter_by(email=email).first()
    if user and user.check_password(password):
        return user
    return None
