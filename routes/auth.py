import logging
import datetime
import jwt
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from services.database import get_collection, is_connected
from backend.config import Config

logger = logging.getLogger(__name__)

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    if not is_connected():
        return jsonify({"error": "Database not available"}), 503

    data = request.get_json()
    if not data or "email" not in data or "password" not in data:
        return jsonify({"error": "Missing email or password"}), 400

    email = data["email"].strip().lower()
    password = data["password"]

    if len(password) < 6:
        return jsonify({"error": "Password must be at least 6 characters"}), 400

    try:
        users_collection = get_collection("users")
        
        # Check if user already exists
        if users_collection.find_one({"email": email}):
            return jsonify({"error": "User with this email already exists"}), 409

        # Hash password and save
        hashed_password = generate_password_hash(password)
        new_user = {
            "email": email,
            "password": hashed_password,
            "created_at": datetime.datetime.now(datetime.timezone.utc)
        }
        
        result = users_collection.insert_one(new_user)
        user_id = str(result.inserted_id)
        
        # Generate token immediately after registration
        token = jwt.encode({
            'user_id': user_id,
            'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=7)
        }, Config.SECRET_KEY, algorithm="HS256")

        return jsonify({"message": "User created successfully", "token": token, "user": {"email": email}}), 201

    except Exception as e:
        logger.error(f"Registration failed: {e}")
        return jsonify({"error": "Registration failed"}), 500


@auth_bp.route("/login", methods=["POST"])
def login():
    if not is_connected():
        return jsonify({"error": "Database not available"}), 503

    data = request.get_json()
    if not data or "email" not in data or "password" not in data:
        return jsonify({"error": "Missing email or password"}), 400

    email = data["email"].strip().lower()
    password = data["password"]

    try:
        users_collection = get_collection("users")
        user = users_collection.find_one({"email": email})

        if not user or not check_password_hash(user["password"], password):
            return jsonify({"error": "Invalid email or password"}), 401

        # Generate JWT token
        token = jwt.encode({
            'user_id': str(user["_id"]),
            'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=7)
        }, Config.SECRET_KEY, algorithm="HS256")

        return jsonify({"message": "Login successful", "token": token, "user": {"email": email}}), 200

    except Exception as e:
        logger.error(f"Login failed: {e}")
        return jsonify({"error": "Login failed"}), 500
