"""
Authentication routes: Login and signup endpoints.
"""
from flask import Blueprint, request, jsonify
from services.user_service import UserService

auth_bp = Blueprint('auth', __name__, url_prefix='/api')


@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Login endpoint.
    
    Request JSON:
        - username: str
        - password: str
    
    Returns:
        User dict on success, error message on failure
    """
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'error': 'Missing username or password'}), 400
    
    user = UserService.authenticate(username, password)
    if not user:
        return jsonify({'error': 'Invalid credentials'}), 401
    
    return jsonify(user), 200


@auth_bp.route('/signup', methods=['POST'])
def signup():
    """
    Signup endpoint.
    
    Request JSON:
        - username: str
        - password: str
        - display_name: str
        - email: str
    
    Returns:
        New user dict on success, error message on failure
    """
    data = request.json
    username = data.get('username')
    password = data.get('password')
    display_name = data.get('display_name')
    email = data.get('email')
    
    if not all([username, password, display_name, email]):
        return jsonify({'error': 'Missing required fields (username, password, display name, email)'}), 400
    
    user = UserService.create_user(username, password, display_name, email)
    if not user:
        return jsonify({'error': 'Username or Email already exists'}), 409
    
    return jsonify(user), 201
