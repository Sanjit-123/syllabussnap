"""
SyllabusSnap API — Main Application Entry Point
"""
import os
import sys
import logging
from flask import Flask, jsonify
from flask_cors import CORS

# Ensure project root is in Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from backend.config import Config
from routes.analyze import analyze_bp
from routes.history import history_bp
from services.database import init_db, is_connected, close_db

# --- Logging ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%H:%M:%S"
)
logger = logging.getLogger(__name__)


def create_app():
    """Application factory pattern."""
    app = Flask(__name__)
    app.config.from_object(Config)

    # --- CORS ---
    CORS(app, origins=Config.ALLOWED_ORIGINS)

    # --- Ensure uploads directory exists ---
    os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)

    # --- MongoDB ---
    db_connected = init_db(Config.MONGO_URI, Config.MONGO_DB_NAME)
    if not db_connected:
        logger.warning("⚠️  Running WITHOUT database — analyses will NOT be persisted.")

    # --- Register Blueprints ---
    app.register_blueprint(analyze_bp, url_prefix="/api")
    app.register_blueprint(history_bp, url_prefix="/api")

    # --- Health Check ---
    @app.route("/")
    def health():
        return jsonify({
            "status": "running",
            "service": "SyllabusSnap API",
            "version": "1.0.0",
            "database": "connected" if is_connected() else "disconnected"
        })

    # --- Global Error Handlers ---
    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"error": "Endpoint not found"}), 404

    @app.errorhandler(413)
    def file_too_large(e):
        return jsonify({"error": "File too large. Maximum size is 10MB."}), 413

    @app.errorhandler(500)
    def internal_error(e):
        logger.error(f"Internal server error: {e}")
        return jsonify({"error": "Internal server error"}), 500

    # --- Cleanup ---
    @app.teardown_appcontext
    def cleanup(exception=None):
        pass  # Connection pooling handles this

    logger.info("🚀 SyllabusSnap API initialized successfully")
    return app


# --- Entry Point ---
app = create_app()

if __name__ == "__main__":
    try:
        app.run(debug=Config.DEBUG, port=5000, host="0.0.0.0")
    finally:
        close_db()