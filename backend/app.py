"""
Ranked Arena Backend - Flask + SocketIO Application
"""
import eventlet
eventlet.monkey_patch()

from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO
import config
from routes.auth import auth_bp
from routes.user import user_bp
from routes.leaderboard import leaderboard_bp
from sockets.matchmaking import register_matchmaking_handlers
from sockets.game import register_game_handlers

def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)
    app.config['SECRET_KEY'] = config.SECRET_KEY
    
    # Configure CORS - Cho phép Frontend kết nối
    CORS(app, resources={r"/*": {"origins": config.FRONTEND_ORIGIN}}, supports_credentials=True)
    
    # Configure SocketIO
    socketio = SocketIO(app, cors_allowed_origins=config.FRONTEND_ORIGIN)
    
    # Register blueprints (API routes)
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(leaderboard_bp)
    
    # Register socket handlers
    register_matchmaking_handlers(socketio)
    register_game_handlers(socketio)
    
    return app, socketio

# --- QUAN TRỌNG: Đưa dòng này RA NGOÀI khối main ---
# Biến này phải nằm ở đây để Gunicorn có thể tìm thấy và import
app, socketio = create_app()

if __name__ == '__main__':
    # Đoạn này chỉ chạy khi bạn test dưới máy local (python app.py)
    socketio.run(app, debug=config.DEBUG, host=config.HOST, port=config.PORT)
