from flask import Blueprint, request, jsonify
from services.airplane_service import *
from sqlalchemy.exc import IntegrityError

airplane_bp = Blueprint('airplane', __name__, url_prefix='/airplanes')

@airplane_bp.route('/', methods=['POST'])
def create():
    try:
        data = request.get_json()
        airplane = create_airplane(data)
        return jsonify({'id': airplane.id, 'model': airplane.model, 'capacity': airplane.capacity}), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@airplane_bp.route('/', methods=['GET'])
def list_all():
    airplanes = get_all_airplanes()
    return jsonify([{'id': a.id, 'model': a.model, 'capacity': a.capacity} for a in airplanes])

@airplane_bp.route('/<int:id>/', methods=['GET'])
def retrieve(id):
    try:
        airplane = get_airplane_by_id(id)
        return jsonify({'id': airplane.id, 'model': airplane.model, 'capacity': airplane.capacity})
    except ValueError as e:
        return jsonify({'error': str(e)}), 404

@airplane_bp.route('/<int:id>/', methods=['PUT'])
def update(id):
    try:
        data = request.get_json()
        airplane = update_airplane(id, data)
        return jsonify({'id': airplane.id, 'model': airplane.model, 'capacity': airplane.capacity})
    except ValueError as e:
        return jsonify({'error': str(e)}), 404

@airplane_bp.route('/<int:id>/', methods=['DELETE'])
def delete(id):
    try:
        delete_airplane(id)
        return '', 204
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
