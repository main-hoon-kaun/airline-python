from database import db

class Airplane(db.Model):
    __tablename__ = 'airplane'
    id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.String(255))
    capacity = db.Column(db.Integer)

    @staticmethod
    def get_next_id():
        # Retrieve the highest current id, start from 1 if no records exist
        current_max_id = Airplane.query.order_by(Airplane.id.desc()).first()
        next_id = (current_max_id.id + 1) if current_max_id else 1  # Start from 1
        return next_id

    def __init__(self, model, capacity):
        self.id = self.get_next_id()  # Assign the incremented ID
        self.model = model
        self.capacity = capacity