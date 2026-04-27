import jwt
import datetime
import os
import pymongo
from flask import Blueprint, request, jsonify, render_template
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from pathlib import Path

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

SECRET_KEY = os.getenv('JWT_SECRET', 'super-secret-key-for-dev')
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")

# MongoDB Setup
try:
    mongo_client = pymongo.MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    db = mongo_client["truthlens"]
    users_col = db["users"]
    
    # Ensure indexes
    users_col.create_index("username", unique=True)
    
    # Ensure default admin exists
    admin_user = users_col.find_one({"username": "admin"})
    if not admin_user:
        users_col.insert_one({
            "username": "admin",
            "password_hash": generate_password_hash("admin"),
            "role": "admin",
            "created_at": datetime.datetime.utcnow().isoformat()
        })
except Exception as e:
    print(f"Auth MongoDB Warning: {e}")
    users_col = None

@auth_bp.route('/restore-original-users-once', methods=['GET'])
def restore_original_users():
    try:
        if users_col is not None:
            # CLEANUP: Drop conflicting email index if it exists
            try:
                users_col.drop_index("email_1")
            except Exception as e:
                print(f"Index drop warning: {e}")

            users_col.delete_many({})
            users_to_restore = [
                {"username": "admin", "password": "admin", "role": "admin"},
                {"username": "Ankit", "password": "admin", "role": "user"},
                {"username": "RajAnkit27", "password": "RajAnkit27@", "role": "user"},
                {"username": "Rajankit27", "password": "RajAnkit27@", "role": "user"},
                {"username": "RajAnkit27-RA", "password": "RajAnkit27@", "role": "user"}
            ]
            for u in users_to_restore:
                # Use update_one with upsert to avoid DuplicateKeyError if some already exist
                users_col.update_one(
                    {"username": u["username"]},
                    {"$set": {
                        "username": u["username"],
                        "password_hash": generate_password_hash(u["password"]),
                        "role": u["role"],
                        "created_at": datetime.datetime.utcnow().isoformat()
                    }},
                    upsert=True
                )
            return "Users restored successfully. You can now login.", 200
        return "Database unavailable", 500
    except Exception as e:
        return str(e), 500

@auth_bp.route('/status', methods=['GET'])
def auth_status():
    if users_col is None:
        return jsonify({"status": "error", "message": "MongoDB not connected"}), 500
    try:
        count = users_col.count_documents({})
        return jsonify({"status": "ok", "user_count": count}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@auth_bp.route('/register', methods=['GET'])
def register_page():
    return render_template('register.html')

@auth_bp.route('/login', methods=['GET'])
def login_page():
    return render_template('login.html')

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json(force=True, silent=True)
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({"error": "Missing username or password"}), 400

    username = data['username']
    password = data['password']
    role = data.get('role', 'user')

    if users_col is None:
        return jsonify({"error": "Database unavailable"}), 500

    try:
        users_col.insert_one({
            "username": username,
            "password_hash": generate_password_hash(password),
            "role": role,
            "created_at": datetime.datetime.utcnow().isoformat()
        })
        return jsonify({"message": "User registered successfully"}), 201
    except pymongo.errors.DuplicateKeyError:
        return jsonify({"error": "Username already exists"}), 409
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json(force=True, silent=True)
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({"error": "Missing username or password"}), 400

    username = data['username']
    password = data['password']

    if users_col is None:
        return jsonify({"error": "Database unavailable"}), 500

    user = users_col.find_one({"username": username})
    
    if user and check_password_hash(user["password_hash"], password):
        token = jwt.encode({
            'user_id': str(user["username"]), # Using username as ID for history persistence
            'username': user['username'],
            'role': user.get('role', 'user'),
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        }, SECRET_KEY, algorithm='HS256')

        return jsonify({"token": token, "role": user.get('role', 'user')}), 200

    return jsonify({"error": "Invalid username or password"}), 401

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]

        if not token:
            return jsonify({'error': 'Token is missing!'}), 401
        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            request.user = data
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token has expired!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token!'}), 401

        return f(*args, **kwargs)
    return decorated

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
        
        if not token:
            return jsonify({'error': 'Admin Token is missing!'}), 401
        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            if data.get('role') != 'admin':
                return jsonify({'error': 'Requires admin privileges!'}), 403
            request.user = data
        except Exception:
            return jsonify({'error': 'Invalid or expired admin token!'}), 401
            
        return f(*args, **kwargs)
    return decorated
