# from flask import Blueprint, request, jsonify
# from services.wallet_service import *
# from sqlalchemy.exc import IntegrityError
# from logger import wallet_logger
# from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

# wallet_bp = Blueprint('wallet', __name__)

# @wallet_bp.route('/create', methods=['POST'])
# @jwt_required()
# def create_wallet_route():
#     try:
#         current_user_id = int(get_jwt_identity())
#         data = request.get_json()
#         data['user_id'] = current_user_id  # Enforce user_id from token, not from body

#         wallet_logger.info(f"Creating wallet for user ID {current_user_id} with data: {data}")
#         wallet = create_wallet(data)
#         wallet_logger.info(f"Created wallet: {wallet}")
#         return jsonify({
#             'id': wallet.id,
#             'balance': str(wallet.balance),
#             'user_id': wallet.user_id
#         }), 201
#     except ValueError as e:
#         wallet_logger.error(f"Wallet creation failed: {str(e)}")
#         return jsonify({'error': str(e)}), 400
#     except IntegrityError as e:
#         wallet_logger.error(f"Integrity error: {str(e)}")
#         return jsonify({'error': 'Database constraint error'}), 400


# @wallet_bp.route('/me', methods=['GET'])
# @jwt_required()
# def get_wallet_for_current_user():
#     try:
#         current_user_id = int(get_jwt_identity())
#         wallet_logger.info(f"Retrieving wallet for current user ID: {current_user_id}")
#         wallet = get_wallet_by_user_id(current_user_id)
#         return jsonify({
#             'id': wallet.id,
#             'balance': str(wallet.balance),
#             'user_id': wallet.user_id
#         })
#     except ValueError as e:
#         wallet_logger.error(f"Wallet not found for user ID {current_user_id}: {str(e)}")
#         return jsonify({'error': str(e)}), 404


# @wallet_bp.route('/user/<int:user_id>', methods=['GET'])
# @jwt_required()
# def get_wallet_by_user_id_route(user_id):
#     claims = get_jwt()
#     role = claims.get('role')

#     if role != 'ADMIN':
#         return jsonify({'error': 'Access denied: Admins only'}), 403

#     try:
#         wallet_logger.info(f"Admin retrieving wallet for user ID: {user_id}")
#         wallet = get_wallet_by_user_id(user_id)
#         return jsonify({
#             'id': wallet.id,
#             'balance': str(wallet.balance),
#             'user_id': wallet.user_id
#         })
#     except ValueError as e:
#         wallet_logger.error(f"Wallet not found for user ID {user_id}: {str(e)}")
#         return jsonify({'error': str(e)}), 404


# @wallet_bp.route('/update', methods=['PUT'])
# @jwt_required()
# def update_wallet_route():
#     try:
#         current_user_id = int(get_jwt_identity())
#         data = request.get_json()
#         data['user_id'] = current_user_id  # Enforce ownership

#         wallet_logger.info(f"Updating wallet for user ID {current_user_id} with data: {data}")
#         wallet = update_wallet(data)
#         return jsonify({
#             'id': wallet.id,
#             'balance': str(wallet.balance),
#             'user_id': wallet.user_id
#         })
#     except ValueError as e:
#         wallet_logger.error(f"Failed to update wallet: {str(e)}")
#         return jsonify({'error': str(e)}), 404
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from services.wallet_service import create_wallet, get_wallet_by_user_id, update_wallet
from sqlalchemy.exc import IntegrityError
from logger import wallet_logger

wallet_bp = Blueprint('wallet', __name__, url_prefix='/api/wallets')

# @wallet_bp.route('/create', methods=['POST'])
# @jwt_required()
# def create_wallet_route():
#     try:
#         # Extract user identity from JWT token
#         current_user = get_jwt_identity()
#         current_user_id = current_user.get("id") if isinstance(current_user, dict) else int(current_user)

#         # Validate incoming request data
#         data = request.get_json()
#         print("Received request data:", data)
#         if not data or not isinstance(data, dict):
#             return jsonify({'error': 'Invalid request format'}), 400
        
#         data['user_id'] = current_user_id  # Enforce user_id from token, not from body
       


#         wallet_logger.info(f"Creating wallet for user ID {current_user_id} with data: {data}")
#         wallet = create_wallet(data)

#         if not wallet:
#             return jsonify({'error': 'Failed to create wallet'}), 500

#         wallet_logger.info(f"Created wallet: {wallet}")
#         return jsonify({
#             'id': wallet.id,
#             'balance': str(wallet.balance),
#             'user_id': wallet.user_id
#         }), 201
#     except IntegrityError as e:
#         wallet_logger.error(f"Integrity error: {str(e)}")
#         return jsonify({'error': 'Database constraint error'}), 400
#     except ValueError as e:
#         wallet_logger.error(f"Wallet creation failed: {str(e)}")
#         return jsonify({'error': str(e)}), 400

@wallet_bp.route('/create', methods=['POST'])
@jwt_required()
def create_wallet_route():
    try:
        current_user = get_jwt_identity()
        current_user_id = current_user.get("id") if isinstance(current_user, dict) else int(current_user)

        # Get and validate request data
        data = request.get_json(force=True)
        print("Parsed JSON:", data)
        if not data or not isinstance(data, dict):
            return jsonify({'error': 'Invalid request format. JSON expected.'}), 400

        # Use "0.00" as default balance if not provided
        balance = data.get('balance', '0.00')
        if not isinstance(balance, str):
            balance = str(balance)  # convert numeric input to string

        # Prepare final payload
        data = {
            'user_id': current_user_id,
            'balance': balance
        }

        wallet_logger.info(f"Creating wallet for user ID {current_user_id} with data: {data}")
        wallet = create_wallet(data)

        if not wallet:
            return jsonify({'error': 'Failed to create wallet'}), 500

        wallet_logger.info(f"Created wallet: {wallet}")
        return jsonify({
            'id': wallet.id,
            'balance': str(wallet.balance),
            'user_id': wallet.user_id
        }), 201

    except IntegrityError as e:
        wallet_logger.error(f"Integrity error: {str(e)}")
        return jsonify({'error': 'Database constraint error'}), 400

    except ValueError as e:
        wallet_logger.error(f"Wallet creation failed: {str(e)}")
        return jsonify({'error': str(e)}), 400
    


@wallet_bp.route('/me', methods=['GET'])
@jwt_required()
def get_wallet_for_current_user():
    try:
        current_user = get_jwt_identity()
        current_user_id = current_user.get("id") if isinstance(current_user, dict) else int(current_user)

        wallet_logger.info(f"Retrieving wallet for user ID {current_user_id}")
        wallet = get_wallet_by_user_id(current_user_id)

        if not wallet:
            return jsonify({'error': 'Wallet not found'}), 404

        return jsonify({
            'id': wallet.id,
            'balance': str(wallet.balance),
            'user_id': wallet.user_id
        })
    except ValueError as e:
        wallet_logger.error(f"Wallet retrieval failed: {str(e)}")
        return jsonify({'error': str(e)}), 404

@wallet_bp.route('/user/<int:user_id>', methods=['GET'])
@jwt_required()
def get_wallet_by_user_id_route(user_id):
    claims = get_jwt()
    role = claims.get('role')

    # if role != 'ADMIN':
    #     return jsonify({'error': 'Access denied: Admins only'}), 403

    try:
        wallet_logger.info(f"Admin retrieving wallet for user ID {user_id}")
        wallet = get_wallet_by_user_id(user_id)

        if not wallet:
            return jsonify({'error': 'Wallet not found'}), 404

        return jsonify({
            'id': wallet.id,
            'balance': str(wallet.balance),
            'user_id': wallet.user_id
        })
    except ValueError as e:
        wallet_logger.error(f"Wallet retrieval failed: {str(e)}")
        return jsonify({'error': str(e)}), 404

@wallet_bp.route('/update', methods=['PUT'])
@jwt_required()
def update_wallet_route():
    try:
        current_user = get_jwt_identity()
        current_user_id = current_user.get("id") if isinstance(current_user, dict) else int(current_user)

        data = request.get_json()

        if not data or not isinstance(data, dict):
            return jsonify({'error': 'Invalid request format'}), 400

        # Ensure users can only update their own wallet
        if 'user_id' in data and data['user_id'] != current_user_id:
            return jsonify({'error': "Access denied: Cannot update another user's wallet"}), 403

        wallet_logger.info(f"Updating wallet for user ID {current_user_id} with data: {data}")
        wallet = update_wallet(data)

        if not wallet:
            return jsonify({'error': 'Wallet update failed'}), 404

        return jsonify({
            'id': wallet.id,
            'balance': str(wallet.balance),
            'user_id': wallet.user_id
        })
    except ValueError as e:
        wallet_logger.error(f"Wallet update failed: {str(e)}")
        return jsonify({'error': str(e)}), 404