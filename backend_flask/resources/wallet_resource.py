from flask import Blueprint, request, jsonify
from services.wallet_service import *
from sqlalchemy.exc import IntegrityError
from logger import wallet_logger  # Import your custom logger

wallet_bp = Blueprint('wallet', __name__)

@wallet_bp.route('/create', methods=['POST'])
def create_wallet_route():
    try:
        data = request.get_json()
        wallet_logger.info(f"Creating wallet with data: {data}")
        wallet = create_wallet(data)
        wallet_logger.info(f"Created wallet: {wallet}")
        return jsonify({
            'id': wallet.id,
            'balance': str(wallet.balance),
            'user_id': wallet.user_id
        }), 201
    except ValueError as e:
        wallet_logger.error(f"Wallet creation failed: {str(e)}")
        return jsonify({'error': str(e)}), 400
    except IntegrityError as e:
        wallet_logger.error(f"Integrity error: {str(e)}")
        return jsonify({'error': 'Database constraint error'}), 400

@wallet_bp.route('/user/<int:user_id>', methods=['GET'])
def get_wallet_by_user_id_route(user_id):
    try:
        wallet_logger.info(f"Retrieving wallet for user ID: {user_id}")
        wallet = get_wallet_by_user_id(user_id)
        return jsonify({
            'id': wallet.id,
            'balance': str(wallet.balance),
            'user_id': wallet.user_id
        })
    except ValueError as e:
        wallet_logger.error(f"Wallet not found for user ID {user_id}: {str(e)}")
        return jsonify({'error': str(e)}), 404

@wallet_bp.route('/update', methods=['PUT'])
def update_wallet_route():
    try:
        data = request.get_json()
        wallet_logger.info(f"Updating wallet with data: {data}")
        wallet = update_wallet(data)
        return jsonify({
            'id': wallet.id,
            'balance': str(wallet.balance),
            'user_id': wallet.user_id
        })
    except ValueError as e:
        wallet_logger.error(f"Failed to update wallet: {str(e)}")
        return jsonify({'error': str(e)}), 404
