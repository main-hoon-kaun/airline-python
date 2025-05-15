from flask import Blueprint, request, jsonify
from services.airport_service import *
from sqlalchemy.exc import IntegrityError
from logger import airport_logger  # Import logger
from flask_jwt_extended import jwt_required

airport_bp = Blueprint('airport', __name__)

@airport_bp.route('/', methods=['POST'])
@jwt_required()
def create():
    try:
        data = request.get_json()
        airport_logger.info(f"Creating airport with data: {data}")
        airport = create_airport(data)
        airport_logger.info(f"Created airport: {airport}")
        return jsonify({
            'id': airport.id,
            'name': airport.name,
            'code': airport.code,
            'city': airport.city,
            'country': airport.country
        }), 201
    except ValueError as e:
        airport_logger.error(f"Failed to create airport: {str(e)}")
        return jsonify({'error': str(e)}), 400

@airport_bp.route('/', methods=['GET'])
@jwt_required()
def list_all():
    airport_logger.info("Listing all airports")
    airports = get_all_airports()
    return jsonify([{
        'id': a.id,
        'name': a.name,
        'code': a.code,
        'city': a.city,
        'country': a.country
    } for a in airports])

@airport_bp.route('/<int:id>/', methods=['GET'])
@jwt_required()
def retrieve(id):
    try:
        airport_logger.info(f"Retrieving airport with ID: {id}")
        airport = get_airport_by_id(id)
        return jsonify({
            'id': airport.id,
            'name': airport.name,
            'code': airport.code,
            'city': airport.city,
            'country': airport.country
        })
    except ValueError as e:
        airport_logger.error(f"Airport with ID {id} not found: {str(e)}")
        return jsonify({'error': str(e)}), 404

@airport_bp.route('/<int:id>/', methods=['PUT'])
@jwt_required()
def update(id):
    try:
        data = request.get_json()
        airport_logger.info(f"Updating airport with ID {id} using data: {data}")
        airport = update_airport(id, data)
        return jsonify({
            'id': airport.id,
            'name': airport.name,
            'code': airport.code,
            'city': airport.city,
            'country': airport.country
        })
    except ValueError as e:
        airport_logger.error(f"Failed to update airport ID {id}: {str(e)}")
        return jsonify({'error': str(e)}), 404

@airport_bp.route('/<int:id>/', methods=['DELETE'])
@jwt_required()
def delete(id):
    try:
        airport_logger.info(f"Deleting airport with ID: {id}")
        delete_airport(id)
        airport_logger.info(f"Successfully deleted airport ID {id}")
        return '', 204
    except ValueError as e:
        airport_logger.error(f"Failed to delete airport ID {id}: {str(e)}")
        return jsonify({'error': str(e)}), 404
