from models.user_model import User
from database import db
from werkzeug.security import generate_password_hash
from models.user_model import check_password_hash

# def create_user(username, email, password, role='CUSTOMER'):
#     hashed_password = generate_password_hash(password)
#     user = User(username=username, email=email, password=hashed_password, role=role)
#     db.session.add(user)
#     db.session.commit()
#     return user
def create_user(username, email, password, role='CUSTOMER'):
    user = User(username=username, email=email, password=password, role=role)  # FIXED
    db.session.add(user)
    db.session.commit()
    return user

# def create_user(username, email, password, role='CUSTOMER'):
#     hashed_password = generate_password_hash(password)
#     user = User(username=username, email=email, password_hash=hashed_password, role=role)  # FIXED
#     db.session.add(user)
#     db.session.commit()
#     return user

def authenticate_user(email, password):
    user = User.query.filter_by(email=email).first()
    if user and check_password_hash(user.password_hash, password):  # FIXED
        return user
    return None
