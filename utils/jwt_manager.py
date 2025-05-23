import jwt
import datetime
from functools import wraps
from flask import request, jsonify

SECRET_KEY = "supersecreto123"

def generate_token(username):
    payload = {
        'username': username,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')

def decode_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload['username']
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return None

def jwt_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get("Authorization", "").replace("Bearer ", "")
        username = decode_token(token)
        if not username:
            return jsonify({"message": "Token inválido o expirado"}), 401
        return f(username, *args, **kwargs)
    return decorated_function
