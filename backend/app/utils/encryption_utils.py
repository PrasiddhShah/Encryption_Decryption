# app/utils/encryption_utils.py
import os
from cryptography.fernet import Fernet
from flask import current_app

def get_cipher_suite():
    key = current_app.config['ENCRYPTION_KEY']
    if not key:
        raise ValueError("Encryption key not found in environment variables.")
    return Fernet(key.encode())

def encrypt_text(plain_text):
    cipher_suite = get_cipher_suite()
    encrypted_text = cipher_suite.encrypt(plain_text.encode('utf-8'))
    return encrypted_text.decode('utf-8')

def decrypt_text(encrypted_text):
    cipher_suite = get_cipher_suite()
    decrypted_text = cipher_suite.decrypt(encrypted_text.encode('utf-8'))
    return decrypted_text.decode('utf-8')
