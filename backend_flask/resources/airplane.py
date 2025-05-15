# resources/airplane_resource.py
from flask import Blueprint, request, jsonify
from services.airplane_service import *
from sqlalchemy.exc import IntegrityError
from logger import airplane_logger # Import logger
from flask_jwt_extended import jwt_required

airplane_bp = Blueprint('airplane', __name__)

@airplane_bp.route('/', methods=['POST'])
@jwt_required()
def create():
    try:
        data = request.get_json()
        airplane = create_airplane(data)
        return jsonify({'id': airplane.id, 'model': airplane.model, 'capacity': airplane.capacity}), 201
    except ValueError as e:
        airplane_logger.error(f"Validation Error: {str(e)}")
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        airplane_logger.error(f"Unexpected Error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@airplane_bp.route('/', methods=['GET'])
@jwt_required()
def list_all():
    try:
        airplanes = get_all_airplanes()
        return jsonify([{'id': a.id, 'model': a.model, 'capacity': a.capacity} for a in airplanes])
    except Exception as e:
        airplane_logger.error(f"Error retrieving airplanes: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@airplane_bp.route('/<int:id>/', methods=['GET'])
@jwt_required()
def retrieve(id):
    try:
        airplane = get_airplane_by_id(id)
        return jsonify({'id': airplane.id, 'model': airplane.model, 'capacity': airplane.capacity})
    except ValueError as e:
        airplane_logger.error(f"Airplane not found: {str(e)}")
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        airplane_logger.error(f"Unexpected Error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@airplane_bp.route('/<int:id>/', methods=['PUT'])
# @jwt_required()
def update(id):
    try:
        data = request.get_json()
        airplane = update_airplane(id, data)
        return jsonify({'id': airplane.id, 'model': airplane.model, 'capacity': airplane.capacity})
    except ValueError as e:
        airplane_logger.error(f"Airplane not found for update: {str(e)}")
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        airplane_logger.error(f"Unexpected Error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@airplane_bp.route('/<int:id>/', methods=['DELETE'])
# @jwt_required()
def delete(id):
    try:
        delete_airplane(id)
        return '', 204
    except ValueError as e:
        airplane_logger.error(f"Airplane not found for deletion: {str(e)}")
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        airplane_logger.error(f"Unexpected Error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500
