from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager # Added
import logging # Added
from logging.handlers import RotatingFileHandler # Added
import os # Added for logging path

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager() # Added
login_manager.login_view = 'auth.login' # Added

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app) # Added

    # Logging configuration
    if not app.debug and not app.testing: # Only configure file logging in production/non-debug
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/app.log', maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('Appointment Scheduler startup')


    # Registrar Blueprints
    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    from app.calendar_api import bp as calendar_api_bp # Added
    app.register_blueprint(calendar_api_bp, url_prefix='/api/calendar') # Added

    return app

from app.models import paciente, cita, credencial, user
from app.models.user import User # Added for user_loader

@login_manager.user_loader # Added
def load_user(user_id): # Added
    return User.query.get(int(user_id)) # Added