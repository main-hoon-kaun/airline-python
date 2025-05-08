from flask import Flask
from database import db
from resources.airplane  import airplane_bp
from resources.airport_resource import airport_bp 
from resources.auth_resource import auth_bp
import secrets
from flask_jwt_extended import JWTManager
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'oracle+oracledb://system:12345@localhost:1521/?service_name=xe'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = secrets.token_hex(32)
jwt = JWTManager(app)
db.init_app(app)
# Register your modules blueprints here
app.register_blueprint(airplane_bp)
app.register_blueprint(airport_bp)
app.register_blueprint(auth_bp) 

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # This line is for creating Required Tables
    app.run(debug=True, port=8000)