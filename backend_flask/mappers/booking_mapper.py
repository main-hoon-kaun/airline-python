def to_booking_response_dto(booking):
    return {
        'id': booking.id,
        'bookingTime': booking.booking_time.isoformat() if booking.booking_time else None,
        'seatClass': booking.seat_class,
        'numberOfSeats': booking.number_of_seats,
        'status': booking.status,
        'totalPrice': booking.total_price,
        'flight': to_flight_info(booking.flight),
        'user': to_user_info(booking.user),
        'passengers': [to_passenger_info(p) for p in booking.passengers]
    }
 
def to_flight_info(flight):
    return {
        'id': flight.id,
        'airline': flight.airplane.model if flight.airplane else None,
        'flightNumber': flight.flight_number,
        'origin': to_airport_info(flight.departure_airport),
        'destination': to_airport_info(flight.arrival_airport),
        'departureTime': flight.departure_time.isoformat() if flight.departure_time else None,
        'arrivalTime': flight.arrival_time.isoformat() if flight.arrival_time else None
    }
 
def to_user_info(user):
    return {
        'id': user.id,
        'name': user.username,
        'email': user.email
    }
 
def to_passenger_info(passenger):
    return {
        'id': passenger.id,
        'fullName': passenger.full_name,
        'email': passenger.email,
        'passportNumber': passenger.passport_number,
        'dateOfBirth': passenger.date_of_birth.isoformat() if passenger.date_of_birth else None
    }

def to_airport_info(airport):
    return {
        'id': airport.id,
        'name': airport.name,
        'code': airport.code,
        'country': airport.country,
        'city': airport.city,
    }