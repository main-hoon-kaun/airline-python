from database import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password_hash = db.Column(db.String(256), nullable=False)  # Increase size to 256 characters
    role = db.Column(db.String(20), default='CUSTOMER')
    # wallet = db.relationship('Wallet', uselist=False, back_populates='user')
    # bookings = db.relationship('Booking', back_populates='user')

    @staticmethod
    def get_next_id():
        current_max = db.session.query(db.func.max(User.id)).scalar()
        return (current_max or 0) + 1

    def set_password(self, password):
        # Use pbkdf2:sha256 for the correct hash method
        self.password_hash = generate_password_hash(password, method='pbkdf2:sha256')

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __init__(self, username, email, password, role='CUSTOMER'):
        self.id = User.get_next_id()
        self.username = username
        self.email = email
        self.set_password(password)
        self.role = role

    def __repr__(self):
        return f"<User {self.username}>"
