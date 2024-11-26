# app/__init__.py
from flask import Flask
from .config import Config
from .extensions import db, migrate, cors
from .routes.auth import auth_bp
from .routes.encryption import encryption_bp
from .routes.data import data_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app, resources={r"/*": {"origins": app.config['CORS_ORIGINS']}})

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(encryption_bp)
    app.register_blueprint(data_bp)

    return app
