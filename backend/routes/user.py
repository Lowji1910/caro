"""
User routes: Profile and account management endpoints.
"""
from flask import Blueprint, request, jsonify
from services.user_service import UserService
from services.match_service import MatchService

user_bp = Blueprint('user', __name__, url_prefix='/api')


@user_bp.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """
    Get user profile by ID.
    
    Returns:
        User dict or 404 error
    """
    user = UserService.get_user_by_id(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify(user), 200


@user_bp.route('/profile/<int:user_id>', methods=['PUT'])
def update_profile(user_id):
    """
    Update user profile.
    
    Request JSON:
        - full_name: str (optional)
        - display_name: str (optional)
        - date_of_birth: str (optional)
        - bio: str (optional)
        - avatar_url: str (optional)
    
    Returns:
        Updated user dict
    """
    data = request.json or {}
    user = UserService.update_profile(user_id, **data)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify(user), 200


@user_bp.route('/change-password/<int:user_id>', methods=['POST'])
def change_password(user_id):
    """
    Change user password.
    
    Request JSON:
        - oldPassword: str
        - newPassword: str
    
    Returns:
        Success message or error
    """
    data = request.json
    old_password = data.get('oldPassword')
    new_password = data.get('newPassword')
    
    if not old_password or not new_password:
        return jsonify({'error': 'Missing password fields'}), 400
    
    if UserService.change_password(user_id, old_password, new_password):
        return jsonify({'message': 'Password changed successfully'}), 200
    
    return jsonify({'error': 'Invalid old password'}), 401


@user_bp.route('/history/<int:user_id>', methods=['GET'])
def get_match_history(user_id):
    """
    Get user's match history.
    
    Query params:
        - limit: int (default 20)
    
    Returns:
        List of match records
    """
    limit = request.args.get('limit', 20, type=int)
    history = MatchService.get_user_match_history(user_id, limit)
    
    return jsonify(history), 200


@user_bp.route('/stats/<int:user_id>', methods=['GET'])
def get_user_stats(user_id):
    """
    Get user's match statistics.
    
    Returns:
        Dict with win/loss/draw counts
    """
    stats = MatchService.get_match_stats(user_id)
    return jsonify(stats), 200


@user_bp.route('/match/<int:match_id>', methods=['GET'])
def get_match_details(match_id):
    """
    Get match details for replay.
    """
    match = MatchService.get_match_details(match_id)
    if not match:
        return jsonify({'error': 'Match not found'}), 404
    return jsonify(match), 200


@user_bp.route('/public/<int:user_id>', methods=['GET'])
def get_public_profile(user_id):
    """
    Get public user profile.
    """
    user = UserService.get_public_profile(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify(user), 200
