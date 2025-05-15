from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token, jwt_required,
    get_jwt_identity, get_jwt
)
from services.user_service import create_user, authenticate_user
from models.user_model import User
from database import db

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    role = data.get('role', 'CUSTOMER')

    if User.query.filter((User.username == username) | (User.email == email)).first():
        return jsonify({'message': 'User already exists'}), 400

    user = create_user(username, email, password, role)

    # access_token = create_access_token(
    #     identity=str(user.id),
    #     additional_claims={
    #         'username': user.username,
    #         'role': user.role
    #     }
    # )

    access_token = create_access_token(identity=str(user.id), additional_claims={
    'username': user.username,
    'role': user.role,
    'email': user.email
})


    return jsonify({
        'token': access_token,
        'id': user.id,
        'username': user.username,
        'role': user.role,
        'email': user.email
    }), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = authenticate_user(email, password)
    if not user:
        return jsonify({'message': 'Invalid credentials'}), 401

    access_token = create_access_token(
        identity=str(user.id),
        additional_claims={
            'username': user.username,
            'role': user.role,
            'email': user.email
        }
    )

    return jsonify({
        'token': access_token,
        'id': user.id,
        'username': user.username,
        'role': user.role,
        'email': user.email
    }), 200


@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def me():
    identity = get_jwt_identity()  # This is user ID as string
    claims = get_jwt()             # Additional data: username, role

    return jsonify({
        'id': identity,
        'username': claims.get('username'),
        'role': claims.get('role'),
        'email': claims.get('email')
    })
