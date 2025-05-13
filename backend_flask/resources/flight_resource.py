from flask import Blueprint, request, jsonify
from services.flight_service import create_flight, get_all_flights, get_flight_by_id, update_flight, delete_flight
from logger import flight_logger
from datetime import datetime

flight_bp = Blueprint('flight', __name__)

def serialize_flight(flight):
    return {
        'id': flight.id,
        'flightNumber': flight.flight_number or '',
        'origin': {
            'id': flight.departure_airport.id,
            'name': flight.departure_airport.name,
            'code': flight.departure_airport.code,
        } if flight.departure_airport else None,
        'destination': {
            'id': flight.arrival_airport.id,
            'name': flight.arrival_airport.name,
            'code': flight.arrival_airport.code,
        } if flight.arrival_airport else None,
        'airplane': {
            'id': flight.airplane.id,
            'model': flight.airplane.model,
            'capacity': flight.airplane.capacity
        } if flight.airplane else None,
        'departureTime': flight.departure_time.isoformat() if isinstance(flight.departure_time, datetime) else '',
        'arrivalTime': flight.arrival_time.isoformat() if isinstance(flight.arrival_time, datetime) else '',
        'price': flight.price or 0
    }

def validate_string_field(field_value, field_name):
    if field_value is None or not isinstance(field_value, str):
        raise ValueError(f"Invalid {field_name}: must be a non-empty string.")
    return field_value.strip()

@flight_bp.route('/', methods=['POST'])
def create():
    try:
        flight_logger.info("Received request to create flight")
        data = request.get_json()
        flight_logger.info(f"Raw payload: {data}")

        required_fields = [
            'flight_number', 'departure_airport_id', 'arrival_airport_id',
            'airplane_id', 'departure_time', 'arrival_time', 'price'
        ]
        for field in required_fields:
            if field not in data:
                flight_logger.warning(f"Missing required field: {field}")
                return jsonify({'error': f'Missing required field: {field}'}), 400

        data['flight_number'] = validate_string_field(data['flight_number'], 'flight_number')
        data['departure_time'] = datetime.fromisoformat(data['departure_time'])
        data['arrival_time'] = datetime.fromisoformat(data['arrival_time'])

        flight_logger.info(f"Final validated data before creation: {data}")
        flight = create_flight(data)
        flight_logger.info(f"Successfully created flight: {flight}")

        return jsonify(serialize_flight(flight)), 201

    except ValueError as e:
        flight_logger.error(f"Validation error: {str(e)}")
        return jsonify({'error': str(e)}), 400

    except Exception as e:
        import traceback
        flight_logger.error(f"Unexpected error during flight creation: {str(e)}")
        flight_logger.error(traceback.format_exc())
        return jsonify({'error': 'Unexpected error occurred while creating the flight'}), 500

@flight_bp.route('/', methods=['GET'])
def list_all():
    try:
        flight_logger.info("Listing all flights")
        flights = get_all_flights()
        return jsonify([serialize_flight(f) for f in flights])
    except Exception as e:
        flight_logger.error(f"Error listing flights: {str(e)}")
        return jsonify({'error': 'Could not list flights'}), 500

@flight_bp.route('/<int:id>/', methods=['GET'])
def retrieve(id):
    try:
        flight_logger.info(f"Retrieving flight with ID: {id}")
        flight = get_flight_by_id(id)
        return jsonify(serialize_flight(flight))
    except ValueError as e:
        flight_logger.error(f"Flight with ID {id} not found: {str(e)}")
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        flight_logger.error(f"Unexpected error: {str(e)}")
        return jsonify({'error': 'Unexpected error occurred while retrieving the flight'}), 500
@flight_bp.route('/<int:id>/', methods=['PUT'])
def update(id):
    try:
        data = request.get_json()
        required_fields = [
            'flight_number', 'departure_airport_id', 'arrival_airport_id',
            'airplane_id', 'departure_time', 'arrival_time', 'price'
        ]
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400

        flight_logger.info(f"Updating flight with ID {id} using data: {data}")

        # Log the types and values of the datetime fields
        flight_logger.info(f"Type of departure_time: {type(data['departure_time'])}, Value: {data['departure_time']}")
        flight_logger.info(f"Type of arrival_time: {type(data['arrival_time'])}, Value: {data['arrival_time']}")

        # Clean up and convert the times
        dep_time = data['departure_time'].strip()
        arr_time = data['arrival_time'].strip()

        try:
            # Try using fromisoformat
            if isinstance(dep_time, str):
                data['departure_time'] = datetime.fromisoformat(dep_time)
            elif isinstance(dep_time, datetime):
                data['departure_time'] = dep_time
            else:
                raise ValueError(f"Invalid type for departure_time: {type(dep_time).__name__}")

            if isinstance(arr_time, str):
                data['arrival_time'] = datetime.fromisoformat(arr_time)
            elif isinstance(arr_time, datetime):
                data['arrival_time'] = arr_time
            else:
                raise ValueError(f"Invalid type for arrival_time: {type(arr_time).__name__}")
        
        except ValueError as e:
            # Handle the ValueError if fromisoformat fails
            flight_logger.warning(f"Error using fromisoformat, falling back to strptime: {str(e)}")

            # If fromisoformat fails, try using strptime with a known format
            try:
                data['departure_time'] = datetime.strptime(dep_time, "%Y-%m-%dT%H:%M:%S")
                data['arrival_time'] = datetime.strptime(arr_time, "%Y-%m-%dT%H:%M:%S")
            except Exception as ex:
                flight_logger.error(f"Failed to parse date using strptime: {str(ex)}")
                return jsonify({'error': f"Invalid date format: {str(ex)}"}), 400

        flight = update_flight(id, data)
        return jsonify(serialize_flight(flight)), 200

    except Exception as e:
        flight_logger.error(f"Unexpected error: {str(e)}")
        return jsonify({'error': 'Unexpected error occurred while updating the flight'}), 500
@flight_bp.route('/<int:id>/', methods=['DELETE'])
def delete(id):
    try:
        flight_logger.info(f"Deleting flight with ID: {id}")
        delete_flight(id)
        flight_logger.info(f"Successfully deleted flight ID {id}")
        return '', 204
    except ValueError as e:
        flight_logger.error(f"Failed to delete flight ID {id}: {str(e)}")
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        flight_logger.error(f"Unexpected error: {str(e)}")
        return jsonify({'error': 'Unexpected error occurred while deleting the flight'}), 500
