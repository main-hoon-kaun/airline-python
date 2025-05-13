from datetime import datetime
from database import db

class Booking(db.Model):
    __tablename__ = 'booking'
    
    id = db.Column(db.Integer, primary_key=True)
    booking_time = db.Column(db.DateTime, default=datetime.utcnow)  # Make sure this is DateTime
    seat_class = db.Column(db.String(50))
    number_of_seats = db.Column(db.Integer)
    status = db.Column(db.String(50))
    total_price = db.Column(db.Float)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    flight_id = db.Column(db.Integer, db.ForeignKey('flight.id'))

    user = db.relationship('User', backref='bookings')
    flight = db.relationship('Flight', backref='bookings')
    passengers = db.relationship('Passenger', backref='booking', cascade="all, delete-orphan")

    @staticmethod
    def get_next_id():
        # Retrieve the highest current id, start from 1 if no records exist
        current_max_id = Booking.query.order_by(Booking.id.desc()).first()
        next_id = (current_max_id.id + 1) if current_max_id else 1  # Start from 1 if no records exist
        return next_id

    def __init__(self, booking_time, seat_class, number_of_seats, status, total_price, user, flight):
        self.id = self.get_next_id()  # Assign the incremented ID
        self.booking_time = booking_time if booking_time else datetime.utcnow()  # Ensure valid datetime
        self.seat_class = seat_class
        self.number_of_seats = number_of_seats
        self.status = status
        self.total_price = total_price
        self.user = user
        self.flight = flight
