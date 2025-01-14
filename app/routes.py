from flask import Blueprint, request, jsonify
from flask_cors import CORS
from .models import User, db  # Use relative import
from cryptography.fernet import Fernet
import os
from functools import wraps
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

main_bp = Blueprint('main', __name__)
CORS(main_bp)

# Get Fernet key and master password from .env
FERNET_KEY = os.getenv('FERNET_KEY')
MASTER_PASSWORD = os.getenv('MASTER_PASSWORD', 'admin123')

if not FERNET_KEY:
    raise ValueError("FERNET_KEY not found in environment variables")

try:
    fer = Fernet(FERNET_KEY.encode())
except Exception as e:
    # Generate a new key if the current one is invalid
    new_key = Fernet.generate_key().decode()
    with open('.env', 'w') as f:
        f.write(f'FERNET_KEY={new_key}\n')
        f.write(f'MASTER_PASSWORD={MASTER_PASSWORD}\n')
    fer = Fernet(new_key.encode())

def require_master_password(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        data = request.json
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        if data.get('master_password') != MASTER_PASSWORD:
            return jsonify({'error': 'Invalid master password'}), 401
        return f(*args, **kwargs)
    return decorated_function

@main_bp.route('/')
def index():
    return "Password Manager API is running!"

@main_bp.route('/add', methods=['POST'])
def add_password():
    try:
        data = request.json
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        required_fields = ['application', 'username', 'password']
        missing_fields = [field for field in required_fields if field not in data]
        
        if missing_fields:
            return jsonify({
                'error': f'Missing required fields: {", ".join(missing_fields)}'
            }), 400

        encrypted_password = fer.encrypt(data['password'].encode()).decode()
        
        new_entry = User(
            application=data['application'],
            username=data['username'],
            password=encrypted_password
        )
        
        db.session.add(new_entry)
        db.session.commit()
        
        return jsonify({'message': 'Password saved successfully'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@main_bp.route('/view')
def view_passwords():
    passwords = User.query.all()
    return jsonify([{
        'id': pwd.id,
        'application': pwd.application,
        'username': pwd.username,
        'created_at': pwd.created_at.isoformat()
    } for pwd in passwords]), 200

@main_bp.route('/view/<int:id>', methods=['GET'])
@require_master_password
def view_password(id):
    pwd = User.query.get_or_404(id)
    try:
        decrypted = fer.decrypt(pwd.password.encode()).decode()
        return jsonify({
            'id': pwd.id,
            'application': pwd.application,
            'username': pwd.username,
            'password': decrypted
        }), 200
    except Exception as e:
        return jsonify({'error': f'Decryption error: {str(e)}'}), 500

@main_bp.route('/delete/<int:id>', methods=['DELETE'])
@require_master_password
def delete_password(id):
    pwd = User.query.get_or_404(id)
    try:
        db.session.delete(pwd)
        db.session.commit()
        return jsonify({'message': 'Password deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Deletion error: {str(e)}'}), 500

@main_bp.route('/update/<int:id>', methods=['PUT'])
@require_master_password
def update_password(id):
    data = request.json
    if 'new_password' not in data:
        return jsonify({'error': 'New password not provided'}), 400

    pwd = User.query.get_or_404(id)
    try:
        encrypted_password = fer.encrypt(data['new_password'].encode()).decode()
        pwd.password = encrypted_password
        db.session.commit()
        return jsonify({'message': 'Password updated successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Update error: {str(e)}'}), 500
