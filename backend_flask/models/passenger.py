from database import db
class Passenger(db.Model):
    __tablename__ = 'passenger'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(255))
    email = db.Column(db.String(255))
    date_of_birth = db.Column(db.Date)
    passport_number = db.Column(db.String(50))
    booking_id = db.Column(db.Integer, db.ForeignKey('booking.id'))

    
    @staticmethod
    def get_next_id():
        # Retrieve the highest current id, start from 1 if no records exist
        current_max_id = Passenger.query.order_by(Passenger.id.desc()).first()
        next_id = (current_max_id.id + 1) if current_max_id else 1  # Start from 1
        return next_id

    def __init__(self, full_name, email, date_of_birth, passport_number, booking):
        self.id = self.get_next_id()  # Assign the incremented ID
        self.full_name = full_name
        self.email = email
        self.date_of_birth = date_of_birth
        self.passport_number = passport_number
        self.booking = booking