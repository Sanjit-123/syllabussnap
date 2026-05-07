from functools import wraps
from flask import request, jsonify
import jwt
from backend.config import Config

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # Check if token is passed in headers
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith('Bearer '):
                token = auth_header.split(" ")[1]
        
        if not token:
            return jsonify({'error': 'Token is missing! Please log in.'}), 401
        
        try:
            # Decode token
            data = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
            current_user_id = data['user_id']
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token has expired! Please log in again.'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Token is invalid!'}), 401
            
        return f(current_user_id, *args, **kwargs)
    
    return decorated
