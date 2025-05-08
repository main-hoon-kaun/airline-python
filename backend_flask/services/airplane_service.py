from models.airplane import Airplane
from database import db
from sqlalchemy.exc import IntegrityError

def create_airplane(data):
    if Airplane.query.filter_by(model=data['model']).first():
        raise ValueError("Model already exists")
    
    airplane = Airplane(model=data['model'], capacity=data['capacity'])
    db.session.add(airplane)
    db.session.commit()
    return airplane

def get_all_airplanes():
    return Airplane.query.all()

def get_airplane_by_id(id):
    airplane = Airplane.query.get(id)
    if not airplane:
        raise ValueError("Airplane not found")
    return airplane

def update_airplane(id, data):
    airplane = get_airplane_by_id(id)
    airplane.model = data['model']
    airplane.capacity = data['capacity']
    db.session.commit()
    return airplane

def delete_airplane(id):
    airplane = get_airplane_by_id(id)
    db.session.delete(airplane)
    db.session.commit()
