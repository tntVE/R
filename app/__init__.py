from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager # Added

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

    # Registrar Blueprints
    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    return app

from app.models import paciente, cita, credencial, user
from app.models.user import User # Added for user_loader

@login_manager.user_loader # Added
def load_user(user_id): # Added
    return User.query.get(int(user_id)) # Added