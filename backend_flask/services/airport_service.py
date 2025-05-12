from models.airport import Airport
from database import db
from sqlalchemy.exc import IntegrityError
from logger import airport_logger  # Assuming this is defined

def create_airport(data):
    airport_logger.info(f"Attempting to create airport with data: {data}")
    if Airport.query.filter_by(code=data['code']).first():
        airport_logger.warning(f"Airport with code {data['code']} already exists")
        raise ValueError("Airport with this code already exists")
    
    airport = Airport(
        name=data['name'],
        code=data['code'],
        city=data['city'],
        country=data['country']
    )
    db.session.add(airport)
    db.session.commit()
    airport_logger.info(f"Successfully created airport: {airport}")
    return airport

def get_all_airports():
    airport_logger.info("Fetching all airports from database")
    airports = Airport.query.all()
    airport_logger.info(f"Found {len(airports)} airports")
    return airports

def get_airport_by_id(id):
    airport_logger.info(f"Fetching airport with ID: {id}")
    airport = Airport.query.get(id)
    if not airport:
        airport_logger.warning(f"Airport with ID {id} not found")
        raise ValueError("Airport not found")
    return airport

def update_airport(id, data):
    airport_logger.info(f"Updating airport with ID: {id} using data: {data}")
    airport = get_airport_by_id(id)
    airport.name = data['name']
    airport.code = data['code']
    airport.city = data['city']
    airport.country = data['country']
    db.session.commit()
    airport_logger.info(f"Successfully updated airport ID {id}")
    return airport

def delete_airport(id):
    airport_logger.info(f"Deleting airport with ID: {id}")
    airport = get_airport_by_id(id)
    db.session.delete(airport)
    db.session.commit()
    airport_logger.info(f"Successfully deleted airport ID {id}")
