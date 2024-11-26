# app/decorators.py
from functools import wraps
from flask import session, jsonify, g
from app.models import User

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'message': 'Authentication required.'}), 401
        user = User.query.get(session['user_id'])
        if not user:
            return jsonify({'message': 'Invalid user.'}), 401
        g.user = user
        return f(*args, **kwargs)
    return decorated_function
