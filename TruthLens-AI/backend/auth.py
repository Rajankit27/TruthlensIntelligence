import sqlite3
import jwt
import datetime
import os
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from pathlib import Path

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

SECRET_KEY = os.getenv('JWT_SECRET', 'super-secret-key-for-dev')

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATABASE = PROJECT_ROOT / "backend" / "auth.db"

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    try:
        with get_db() as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL
                )
            ''')
            # Add role column if missing from legacy db
            try:
                conn.execute('SELECT role FROM users LIMIT 1')
            except sqlite3.OperationalError:
                conn.execute('ALTER TABLE users ADD COLUMN role TEXT DEFAULT "user"')
                
            # Add created_at column if missing (Two-step migration for SQLite compatibility)
            try:
                conn.execute('SELECT created_at FROM users LIMIT 1')
            except sqlite3.OperationalError:
                # SQLite 3.x doesn't allow non-constant defaults like CURRENT_TIMESTAMP in ALTER TABLE
                conn.execute('ALTER TABLE users ADD COLUMN created_at TEXT')
                conn.execute("UPDATE users SET created_at = (DATETIME('now')) WHERE created_at IS NULL")
                
            # Ensure admin
            cursor = conn.execute("SELECT id FROM users WHERE role = 'admin'")
            if not cursor.fetchone():
                conn.execute("INSERT OR IGNORE INTO users (username, password_hash, role) VALUES (?, ?, ?)",
                             ("admin", generate_password_hash("admin"), "admin"))
            conn.commit()
    except Exception as e:
        print(f"Warning: Failed to initialize SQLite Database: {e}")

# Initialize DB when module is loaded
init_db()

from flask import Blueprint, request, jsonify, render_template

# ... (skipped imports so it fits in my mental diff)

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
    
    # We can default to 'user' for public registration
    role = data.get('role', 'user')

    try:
        with get_db() as conn:
            conn.execute(
                "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)", 
                (username, generate_password_hash(password), role)
            )
            conn.commit()
        return jsonify({"message": "User registered successfully"}), 201
    except sqlite3.IntegrityError:
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

    with get_db() as conn:
        user = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
    
    if user and check_password_hash(user["password_hash"], password):
        token = jwt.encode({
            'user_id': user["id"],  # Important: Using the integer ID so history reconnects
            'username': user['username'],
            'role': user['role'] if 'role' in user.keys() else 'user',
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        }, SECRET_KEY, algorithm='HS256')

        return jsonify({"token": token, "role": user['role'] if 'role' in user.keys() else 'user'}), 200

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
