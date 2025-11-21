"""
Leaderboard routes: Ranking and leaderboard endpoints.
"""
from flask import Blueprint, request, jsonify
from services.leaderboard_service import LeaderboardService

leaderboard_bp = Blueprint('leaderboard', __name__, url_prefix='/api')


@leaderboard_bp.route('/leaderboard', methods=['GET'])
def get_leaderboard():
    """
    Get global leaderboard.
    
    Query params:
        - limit: int (default 10)
    
    Returns:
        List of top players
    """
    limit = request.args.get('limit', 10, type=int)
    leaderboard = LeaderboardService.get_leaderboard(limit)
    
    return jsonify(leaderboard), 200


@leaderboard_bp.route('/rank/<int:user_id>', methods=['GET'])
def get_user_rank(user_id):
    """
    Get user's rank position.
    
    Returns:
        Dict with rank position
    """
    rank = LeaderboardService.get_user_rank(user_id)
    
    if rank is None:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify({'rank': rank}), 200


@leaderboard_bp.route('/nearby/<int:user_id>', methods=['GET'])
def get_nearby_players(user_id):
    """
    Get players ranked near the given user.
    
    Query params:
        - range: int (default 5, players above and below)
    
    Returns:
        List of nearby players
    """
    range_size = request.args.get('range', 5, type=int)
    nearby = LeaderboardService.get_nearby_players(user_id, range_size)
    
    return jsonify(nearby), 200
