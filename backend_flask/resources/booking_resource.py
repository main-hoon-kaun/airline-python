from flask import Blueprint, request, jsonify
from services.booking_service import *
from logger import booking_logger
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import IntegrityError
booking_bp = Blueprint('booking', __name__)
 
@booking_bp.route('/', methods=['POST'])
#@jwt_required()
#def create():
    #try:
     #   data = request.get_json()
      #  result = create_booking(data)  
       # return jsonify(result), 201
    #except Exception as e:
     #   booking_logger.error(f"Create error: {e}")
      #  return jsonify({'error': str(e)}), 400

@jwt_required()
def create_booking_route():
    try:
        current_user = get_jwt_identity()
        current_user_id = current_user.get("id") if isinstance(current_user, dict) else int(current_user)

        data = request.get_json(force=True)
        booking_logger.info(f"Incoming booking payload: {data}")

        if not data or not isinstance(data, dict):
            return jsonify({'error': 'Invalid request format. JSON expected.'}), 400

        # Inject user_id from JWT
        data['user_id'] = current_user_id
        booking_logger.info(f"Creating booking for user ID {current_user_id} with data: {data}")

        booking = create_booking(data)
        if not booking:
            return jsonify({'error': 'Failed to create booking'}), 500

        response = to_booking_response_dto(booking)
        booking_logger.info(f"Successfully created booking: {response}")

        return jsonify(response), 201

    except IntegrityError as e:
        booking_logger.error(f"Integrity error during booking creation: {str(e)}")
        return jsonify({'error': 'Database constraint error'}), 400

    except ValueError as e:
        booking_logger.error(f"Value error during booking creation: {str(e)}")
        return jsonify({'error': str(e)}), 400

    except Exception as e:
        booking_logger.error(f"Create error: {e}")
        return jsonify({'error': str(e)}), 400


    
@booking_bp.route('/<int:id>/', methods=['PUT'])
@jwt_required()
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
@jwt_required()
def cancel(id):
    try:
        user_email = request.get_json()['user_email']
        cancel_booking(id, user_email)
        return '', 204
    except Exception as e:
        booking_logger.error(f"Cancel error: {e}")
        return jsonify({'error': str(e)}), 400
 
@booking_bp.route('/<int:id>/', methods=['GET'])
@jwt_required()
def retrieve(id):
    try:
        user_email = request.args.get('user_email')
        result = get_booking_by_id(id, user_email)
        return jsonify(result)
    except Exception as e:
        booking_logger.error(f"Retrieve error: {e}")
        return jsonify({'error': str(e)}), 404
 
@booking_bp.route('/', methods=['GET'])
@jwt_required()

def list_all():
    try:
        user_email = request.args.get('user_email')
        role = request.args.get('role')
        result = get_all_bookings(user_email, role)
        return jsonify(result)
    except Exception as e:
        booking_logger.error(f"List error: {e}")
        return jsonify({'error': str(e)}), 400