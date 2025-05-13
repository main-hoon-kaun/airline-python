from models.flight import Flight
from database import db
from logger import flight_logger
from datetime import datetime
from dateutil import parser

def create_flight(data):
    try:
        flight = Flight(
            flight_number=data['flight_number'],
            departure_airport_id=data['departure_airport_id'],
            arrival_airport_id=data['arrival_airport_id'],
            departure_time=data['departure_time'],
            arrival_time=data['arrival_time'],
            airplane_id=data['airplane_id'],
            price=data['price']
        )
        db.session.add(flight)
        db.session.commit()
        return flight
    except Exception as e:
        raise ValueError(f"Invalid flight data: {e}")

def get_all_flights():
    flight_logger.info("Fetching all flights from database")
    flights = Flight.query.all()
    flight_logger.info(f"Found {len(flights)} flights")
    return flights

def get_flight_by_id(id):
    flight_logger.info(f"Fetching flight with ID: {id}")
    flight = Flight.query.get(id)
    if not flight:
        flight_logger.warning(f"Flight with ID {id} not found")
        raise ValueError("Flight not found")
    return flight


def update_flight(id, data):
    flight = get_flight_by_id(id)
    flight.flight_number = data.get('flight_number', flight.flight_number)

    if 'departure_airport_id' in data:
        flight.departure_airport_id = data['departure_airport_id']
    if 'arrival_airport_id' in data:
        flight.arrival_airport_id = data['arrival_airport_id']
    if 'airplane_id' in data:
        flight.airplane_id = data['airplane_id']

    if 'departure_time' in data:
        dt = data['departure_time']
        flight.departure_time = parser.parse(dt) if isinstance(dt, str) else dt

    if 'arrival_time' in data:
        at = data['arrival_time']
        flight.arrival_time = parser.parse(at) if isinstance(at, str) else at

    if 'price' in data:
        flight.price = data['price']

    db.session.commit()
    return flight

def delete_flight(id):
    flight = get_flight_by_id(id)
    db.session.delete(flight)
    db.session.commit()
    flight_logger.info(f"Flight with ID {id} deleted successfully")