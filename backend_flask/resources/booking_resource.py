from flask import Blueprint, request, jsonify
from services.booking_service import *
from logger import booking_logger
 
booking_bp = Blueprint('booking', __name__)
 
@booking_bp.route('/', methods=['POST'])
def create():
    try:
        data = request.get_json()
        result = create_booking(data)  
        return jsonify(result), 201
    except Exception as e:
        booking_logger.error(f"Create error: {e}")
        return jsonify({'error': str(e)}), 400
@booking_bp.route('/<int:id>/', methods=['PUT'])
def update(id):
    try:
        data = request.get_json()
        user_email = data['user_email']
        result = update_booking(id, data, user_email)
        return jsonify(result)
    except Exception as e:
        booking_logger.error(f"Update error: {e}")
        return jsonify({'error': str(e)}), 400
 
@booking_bp.route('/<int:id>/cancel/', methods=['PUT'])
def cancel(id):
    try:
        user_email = request.get_json()['user_email']
        cancel_booking(id, user_email)
        return '', 204
    except Exception as e:
        booking_logger.error(f"Cancel error: {e}")
        return jsonify({'error': str(e)}), 400
 
@booking_bp.route('/<int:id>/', methods=['GET'])
def retrieve(id):
    try:
        user_email = request.args.get('user_email')
        result = get_booking_by_id(id, user_email)
        return jsonify(result)
    except Exception as e:
        booking_logger.error(f"Retrieve error: {e}")
        return jsonify({'error': str(e)}), 404
 
@booking_bp.route('/', methods=['GET'])
def list_all():
    try:
        user_email = request.args.get('user_email')
        role = request.args.get('role')
        result = get_all_bookings(user_email, role)
        return jsonify(result)
    except Exception as e:
        booking_logger.error(f"List error: {e}")
        return jsonify({'error': str(e)}), 400