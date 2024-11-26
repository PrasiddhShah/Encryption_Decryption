# app/config.py
import os
from dotenv import load_dotenv

# Load environment variables from .env
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '..', '.env'))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')  # Ensure you set this environment variable
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgresql://pstgre:1234@localhost:5432/ait670project'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID')  # Set your Google Client ID
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', 'http://localhost:4200').split(',')


