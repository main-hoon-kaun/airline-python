from database import db

class Airport(db.Model):
    __tablename__ = 'airport'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(10), unique=True, nullable=False)
    city = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"<Airport {self.name} ({self.code})>"

    @staticmethod
    def get_next_id():
        # Retrieve the highest current id, start from 1 if no records exist
        current_max_id = Airport.query.order_by(Airport.id.desc()).first()
        next_id = (current_max_id.id + 1) if current_max_id else 1  # Start from 1
        return next_id

    def __init__(self, name, code, city, country):
        self.id = self.get_next_id()  # Assign the incremented ID
        self.name = name
        self.code = code
        self.city = city
        self.country = country
