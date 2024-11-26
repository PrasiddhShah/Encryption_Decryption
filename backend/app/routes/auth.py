from flask import Blueprint, request, jsonify, session, current_app, g
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from werkzeug.security import generate_password_hash, check_password_hash
from ..extensions import db
from ..models import User
from ..decorators import login_required


auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/authenticate', methods=['POST'])
def authenticate():
    data = request.get_json()
    token = data.get('token')

    if not token:
        return jsonify({'message': 'No token provided.'}), 400

    try:
        CLIENT_ID = current_app.config['GOOGLE_CLIENT_ID']
        id_info = id_token.verify_oauth2_token(token, google_requests.Request(), CLIENT_ID)

        # Extract user information
        google_id = id_info['sub']
        email = id_info['email']
        name = id_info.get('name')

        # Check if user exists
        user = User.query.filter_by(google_id=google_id).first()
        if not user:
            return jsonify({'message': 'User not registered. Please register first.'}), 403

        # Store user information in session
        session['user_id'] = user.id

        return jsonify({
            'message': 'Authentication successful',
            'user': {
                'id': user.id,
                'email': user.email,
                'name': user.name
            }
        }), 200

    except ValueError as e:
        # Invalid token
        return jsonify({'message': 'Invalid token', 'error': str(e)}), 400

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    token = data.get('token')

    if not token:
        return jsonify({'message': 'No token provided.'}), 400

    try:
        CLIENT_ID = current_app.config['GOOGLE_CLIENT_ID']
        id_info = id_token.verify_oauth2_token(token, google_requests.Request(), CLIENT_ID)

        # Extract user information
        google_id = id_info['sub']
        email = id_info['email']
        name = id_info.get('name')

        # Check if user already exists
        existing_user = User.query.filter_by(google_id=google_id).first()
        if existing_user:
            return jsonify({'message': 'User already registered. Please log in.'}), 400

        # Create new user
        new_user = User(google_id=google_id, email=email, name=name)
        db.session.add(new_user)
        db.session.commit()

        # Optionally, log the user in
        session['user_id'] = new_user.id

        return jsonify({
            'message': 'Registration successful',
            'user': {
                'id': new_user.id,
                'email': new_user.email,
                'name': new_user.name
            }
        }), 201

    except ValueError as e:
        # Invalid token
        return jsonify({'message': 'Invalid token', 'error': str(e)}), 400

@auth_bp.route('/manual_register', methods=['POST'])
def manual_register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    # Input validation
    if not all([username, email, password]):
        return jsonify({'message': 'Username, email, and password are required.'}), 400

    # Check if user already exists
    existing_user = User.query.filter(
        (User.username == username) | (User.email == email)
    ).first()
    if existing_user:
        return jsonify({'message': 'Username or email already exists.'}), 400

    # Create new user
    new_user = User(username=username, email=email)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()

    # Log the user in
    session['user_id'] = new_user.id

    return jsonify({
        'message': 'Registration successful',
        'user': {
            'id': new_user.id,
            'username': new_user.username,
            'email': new_user.email
        }
    }), 201

@auth_bp.route('/manual_login', methods=['POST'])
def manual_login():
    data = request.get_json()
    username_or_email = data.get('username_or_email')
    password = data.get('password')

    # Input validation
    if not all([username_or_email, password]):
        return jsonify({'message': 'Username/email and password are required.'}), 400

    # Find user by username or email
    user = User.query.filter(
        (User.username == username_or_email) | (User.email == username_or_email)
    ).first()

    if user and user.password_hash and user.check_password(password):
        # Login successful
        session['user_id'] = user.id
        return jsonify({
            'message': 'Login successful',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email
            }
        }), 200
    else:
        # Login failed
        return jsonify({'message': 'Invalid username/email or password.'}), 401

@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    session.pop('user_id', None)
    return jsonify({'message': 'Logged out successfully.'}), 200
