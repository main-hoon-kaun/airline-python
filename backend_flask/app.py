from flask import Flask, request, jsonify
from database import db
from dotenv import load_dotenv
from resources.airplane  import airplane_bp
from resources.airport_resource import airport_bp 
from resources.auth_resource import auth_bp
from resources.flight_resource import flight_bp
from resources.wallet_resource import wallet_bp
from resources.booking_resource import booking_bp

from flask_jwt_extended import JWTManager
from flask_cors import CORS
from datetime import timedelta
import os
load_dotenv()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
app.config['JWT_TOKEN_LOCATION'] = ['headers']
app.config['JWT_HEADER_NAME']     = 'Authorization'
app.config['JWT_HEADER_TYPE']     = 'Bearer'
app.config['JWT_DECODE_ALGORITHMS'] = ['HS256']
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=1)
app.url_map.strict_slashes = False

CORS(app, allow_headers=["Content-Type", "Authorization"],
    expose_headers=["Authorization"],  supports_credentials=True, resources={r"/api/*": {"origins": "http://localhost:8080"}})

jwt = JWTManager(app)
db.init_app(app)

app.register_blueprint(airplane_bp, url_prefix="/api/airplanes")
app.register_blueprint(airport_bp , url_prefix="/api/airports")
app.register_blueprint(auth_bp) 
app.register_blueprint(flight_bp, url_prefix="/api/flights")
app.register_blueprint(wallet_bp, url_prefix="/api/wallets")
app.register_blueprint(booking_bp, url_prefix="/api/bookings")


@app.before_request
def log_headers():
    print("Incoming request headers:", request.headers)

@jwt.unauthorized_loader
def handle_missing_token(error):
    return jsonify({'jwt_error': 'Missing token', 'message': error}), 401

@jwt.invalid_token_loader
def handle_invalid_token(error):
    return jsonify({'jwt_error': 'Invalid token', 'message': error}), 422

@jwt.expired_token_loader
def handle_expired_token(jwt_header, jwt_payload):
    return jsonify({'jwt_error': 'Expired token'}), 401

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # This line is for creating Required Tables
    app.run(debug=True, port=8000)