from database import db

class Flight(db.Model):
    __tablename__ = 'flight'
    
    id = db.Column(db.Integer, primary_key=True)
    flight_number = db.Column(db.String(50), nullable=False)
    departure_airport_id = db.Column(db.Integer, db.ForeignKey('airport.id'), nullable=False)
    arrival_airport_id = db.Column(db.Integer, db.ForeignKey('airport.id'), nullable=False)
    departure_time = db.Column(db.DateTime, nullable=False)
    arrival_time = db.Column(db.DateTime, nullable=False)
    price = db.Column(db.Float, nullable=False)
    airplane_id = db.Column(db.Integer, db.ForeignKey('airplane.id'), nullable=False)

    departure_airport = db.relationship('Airport', foreign_keys=[departure_airport_id])
    arrival_airport = db.relationship('Airport', foreign_keys=[arrival_airport_id])
    airplane = db.relationship('Airplane', backref='flights')

    def __repr__(self):
        return f"<Flight {self.flight_number} from {self.departure_airport.name} to {self.arrival_airport.name}>"

    @staticmethod
    def get_next_id():
        current_max_id = Flight.query.order_by(Flight.id.desc()).first()
        next_id = (current_max_id.id + 1) if current_max_id else 1
        return next_id

    def __init__(self, flight_number, departure_airport_id, arrival_airport_id,
                 departure_time, arrival_time, price, airplane_id):
        self.id = self.get_next_id()
        self.flight_number = flight_number
        self.departure_airport_id = departure_airport_id
        self.arrival_airport_id = arrival_airport_id
        self.departure_time = departure_time
        self.arrival_time = arrival_time
        self.price = price
        self.airplane_id = airplane_id
