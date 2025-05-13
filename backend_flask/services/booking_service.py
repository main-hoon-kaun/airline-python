from models.booking import Booking
from models.passenger import Passenger
from models.user_model import User
from models.flight import Flight
from database import db
from logger import booking_logger
from mappers.booking_mapper import to_booking_response_dto
from sqlalchemy.orm import joinedload
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm.exc import NoResultFound
from dateutil import parser  
def create_booking(data):
    try:
        # Fetch user by ID
        user = User.query.get(data['user_id'])
        if not user:
            raise ValueError("User not found")

        # Fetch flight by ID
        flight = Flight.query.get(data['flight_id'])
        if not flight:
            raise ValueError("Flight not found")
        
        # Convert booking_time from string to datetime object using dateutil parser
        booking_time = parser.isoparse(data['booking_time'])
        
        # Create booking
        booking = Booking(
            booking_time=booking_time,
            seat_class=data['seat_class'],
            number_of_seats=data['number_of_seats'],
            status=data['status'],
            total_price=data['total_price'],
            user=user,
            flight=flight
        )
        
        # Add booking to the session first
        db.session.add(booking)

        # Add passengers to the booking
        for p_data in data['passengers']:
            date_of_birth = datetime.strptime(p_data['date_of_birth'], "%Y-%m-%d")
            
            passenger = Passenger(
                full_name=p_data['full_name'],
                email=p_data['email'],
                date_of_birth=date_of_birth,
                passport_number=p_data['passport_number'],
                booking=booking
            )
            db.session.add(passenger)

        db.session.commit()
 
        booking_logger.info(f"Booking created for user ID {data['user_id']}")
        return to_booking_response_dto(booking)
 
    except Exception as e:
        db.session.rollback()
        booking_logger.error(f"Error creating booking: {e}")
        raise
def update_booking(id, data, user_email):
    try:
        # Fetch booking and ensure user has permission
        booking = Booking.query.get(id)
        if not booking:
            raise ValueError("Booking not found")
        if booking.user.email != user_email:
            raise PermissionError("Unauthorized access")
 
        # Update booking details
        booking.booking_time = data['booking_time']
        booking.seat_class = data['seat_class']
        booking.number_of_seats = data['number_of_seats']
        booking.status = data['status']
        booking.total_price = data['total_price']
 
        # Update passengers
        for p_data in data['passengers']:
            # Check if passenger already exists or is a new one
            passenger = Passenger.query.filter_by(passport_number=p_data['passport_number'], booking_id=id).first()
            if not passenger:
                # If passenger doesn't exist, create a new one
                passenger = Passenger(
                    full_name=p_data['full_name'],
                    email=p_data['email'],
                    date_of_birth=p_data['date_of_birth'],
                    passport_number=p_data['passport_number'],
                    booking=booking
                )
                db.session.add(passenger)
            else:
                # Update existing passenger if necessary
                passenger.full_name = p_data['full_name']
                passenger.email = p_data['email']
                passenger.date_of_birth = p_data['date_of_birth']

        db.session.commit()
        booking_logger.info(f"Booking {id} updated")
        return to_booking_response_dto(booking)
    
    except Exception as e:
        db.session.rollback()
        booking_logger.error(f"Error updating booking: {e}")
        raise


def cancel_booking(id, user_email):
    try:
        # Fetch booking and ensure user has permission
        booking = Booking.query.get(id)
        if not booking:
            raise ValueError("Booking not found")
        if booking.user.email != user_email:
            raise PermissionError("Unauthorized access")
 
        # Update booking status to 'CANCELLED'
        booking.status = 'CANCELLED'
        db.session.commit()
        booking_logger.info(f"Booking {id} cancelled")
    
    except Exception as e:
        db.session.rollback()
        booking_logger.error(f"Error cancelling booking: {e}")
        raise


def get_booking_by_id(id, user_email):
    try:
        # Fetch booking and ensure user has permission
        booking = Booking.query.get(id)
        if not booking:
            raise ValueError("Booking not found")
        if booking.user.email != user_email:
            raise PermissionError("Unauthorized access")
        
        return to_booking_response_dto(booking)
    
    except Exception as e:
        booking_logger.error(f"Error fetching booking {id}: {e}")
        raise


def get_all_bookings(user_email, role):
    try:
        # Ensure role is not None before calling .upper()
        if role and role.upper() == 'ADMIN':
            bookings = Booking.query.all()
        else:
            bookings = Booking.query.join(User).filter(User.email == user_email).all()
        
        return [to_booking_response_dto(b) for b in bookings]
    
    except Exception as e:
        booking_logger.error(f"Error fetching bookings: {e}")
        raise