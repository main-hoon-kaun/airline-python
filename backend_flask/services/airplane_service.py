# services/airplane_service.py
from models.airplane import Airplane
from database import db
from logger import airplane_logger  # Import logger

def create_airplane(data):
    try:
        if Airplane.query.filter_by(model=data['model']).first():
            raise ValueError("Model already exists")
        
        airplane = Airplane(model=data['model'], capacity=data['capacity'])
        db.session.add(airplane)
        db.session.commit()

        airplane_logger.info(f"Airplane created: Model - {airplane.model}, Capacity - {airplane.capacity}")
        return airplane

    except Exception as e:
        airplane_logger.error(f"Error creating airplane: {e}")
        raise

def get_all_airplanes():
    try:
        airplanes = Airplane.query.all()
        airplane_logger.info(f"Retrieved all airplanes: {len(airplanes)} found")
        return airplanes
    except Exception as e:
        airplane_logger.error(f"Error retrieving airplanes: {e}")
        raise

def get_airplane_by_id(id):
    airplane = Airplane.query.get(id)
    if not airplane:
        airplane_logger.warning(f"Airplane with ID {id} not found")
        raise ValueError("Airplane not found")
    airplane_logger.info(f"Retrieved airplane: ID - {airplane.id}, Model - {airplane.model}")
    return airplane

def update_airplane(id, data):
    try:
        airplane = get_airplane_by_id(id)
        airplane.model = data['model']
        airplane.capacity = data['capacity']
        db.session.commit()

        airplane_logger.info(f"Airplane updated: ID - {airplane.id}, New Model - {airplane.model}, New Capacity - {airplane.capacity}")
        return airplane
    except Exception as e:
        airplane_logger.error(f"Error updating airplane: {e}")
        raise

def delete_airplane(id):
    try:
        airplane = get_airplane_by_id(id)
        db.session.delete(airplane)
        db.session.commit()

        airplane_logger.info(f"Airplane deleted: ID - {id}")
    except Exception as e:
        airplane_logger.error(f"Error deleting airplane: {e}")
        raise
