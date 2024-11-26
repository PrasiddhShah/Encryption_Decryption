# app/routes/data.py
from flask import Blueprint, jsonify, session, g
from functools import wraps
from ..extensions import db
from ..models import Data, User

data_bp = Blueprint('data', __name__)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'message': 'Authentication required.'}), 401
        user = User.query.get(user_id)
        if not user:
            return jsonify({'message': 'User not found.'}), 404
        g.user = user
        return f(*args, **kwargs)
    return decorated_function

@data_bp.route('/data', methods=['GET'])
@login_required
def get_user_data():
    data_entries = Data.query.filter_by(user_id=g.user.id).all()
    data_list = [
        {
            'id': entry.id,
            'original_text': entry.original_text,
            'encrypted_text': entry.encrypted_text,
            'decrypted_text': entry.decrypted_text,
            'timestamp': entry.timestamp.isoformat()
        } for entry in data_entries
    ]
    return jsonify({'data_entries': data_list}), 200
