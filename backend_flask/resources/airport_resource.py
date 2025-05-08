from flask import Blueprint, request, jsonify
from services.airport_service import *
from sqlalchemy.exc import IntegrityError

airport_bp = Blueprint('airport', __name__, url_prefix='/airports')

@airport_bp.route('/', methods=['POST'])
def create():
    try:
        data = request.get_json()
        airport = create_airport(data)
        return jsonify({
            'id': airport.id,
            'name': airport.name,
            'code': airport.code,
            'city': airport.city,
            'country': airport.country
        }), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@airport_bp.route('/', methods=['GET'])
def list_all():
    airports = get_all_airports()
    return jsonify([{
        'id': a.id,
        'name': a.name,
        'code': a.code,
        'city': a.city,
        'country': a.country
    } for a in airports])

@airport_bp.route('/<int:id>/', methods=['GET'])
def retrieve(id):
    try:
        airport = get_airport_by_id(id)
        return jsonify({
            'id': airport.id,
            'name': airport.name,
            'code': airport.code,
            'city': airport.city,
            'country': airport.country
        })
    except ValueError as e:
        return jsonify({'error': str(e)}), 404

@airport_bp.route('/<int:id>/', methods=['PUT'])
def update(id):
    try:
        data = request.get_json()
        airport = update_airport(id, data)
        return jsonify({
            'id': airport.id,
            'name': airport.name,
            'code': airport.code,
            'city': airport.city,
            'country': airport.country
        })
    except ValueError as e:
        return jsonify({'error': str(e)}), 404

@airport_bp.route('/<int:id>/', methods=['DELETE'])
def delete(id):
    try:
        delete_airport(id)
        return '', 204
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
