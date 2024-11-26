# app/routes/encryption.py
from flask import Blueprint, request, jsonify, session, g
from functools import wraps
from ..extensions import db
from ..models import Data, User
from ..utils.encryption_utils import encrypt_text, decrypt_text

encryption_bp = Blueprint('encryption', __name__)

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

@encryption_bp.route('/encrypt', methods=['POST'])
@login_required
def encrypt_route():
    data = request.get_json()
    plain_text = data.get('text')
    if not plain_text:
        return jsonify({'message': 'No text provided for encryption.'}), 400

    try:
        encrypted_text = encrypt_text(plain_text)

        # Save to database
        data_entry = Data(
            original_text=plain_text,
            encrypted_text=encrypted_text,
            user_id=g.user.id
        )
        db.session.add(data_entry)
        db.session.commit()

        return jsonify({'encrypted_text': encrypted_text}), 200

    except Exception as e:
        return jsonify({'message': 'Encryption failed.', 'error': str(e)}), 500

@encryption_bp.route('/decrypt', methods=['POST'])
@login_required
def decrypt_route():
    data = request.get_json()
    encrypted_text = data.get('encrypted_text')
    if not encrypted_text:
        return jsonify({'message': 'No encrypted text provided for decryption.'}), 400

    try:
        decrypted_text = decrypt_text(encrypted_text)

        # Update the corresponding data entry
        data_entry = Data.query.filter_by(encrypted_text=encrypted_text, user_id=g.user.id).first()
        if data_entry:
            data_entry.decrypted_text = decrypted_text
            db.session.commit()
            return jsonify({'decrypted_text': decrypted_text}), 200
        else:
            return jsonify({'message': 'Encrypted text not found for the user.'}), 404

    except Exception as e:
        return jsonify({'message': 'Decryption failed.', 'error': str(e)}), 400
