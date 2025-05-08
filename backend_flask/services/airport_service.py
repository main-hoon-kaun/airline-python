from models.airport import Airport
from database import db
from sqlalchemy.exc import IntegrityError

def create_airport(data):
    if Airport.query.filter_by(code=data['code']).first():
        raise ValueError("Airport with this code already exists")
    
    airport = Airport(name=data['name'], code=data['code'], city=data['city'], country=data['country'])
    db.session.add(airport)
    db.session.commit()
    return airport

def get_all_airports():
    return Airport.query.all()

def get_airport_by_id(id):
    airport = Airport.query.get(id)
    if not airport:
        raise ValueError("Airport not found")
    return airport

def update_airport(id, data):
    airport = get_airport_by_id(id)
    airport.name = data['name']
    airport.code = data['code']
    airport.city = data['city']
    airport.country = data['country']
    db.session.commit()
    return airport

def delete_airport(id):
    airport = get_airport_by_id(id)
    db.session.delete(airport)
    db.session.commit()
