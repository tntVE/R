import pytest
from app import create_app, db
from app.models.credencial import Credencial
from app.utils.encrypted_type import EncryptedType
from config import Config
from cryptography.fernet import Fernet
import base64

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SECRET_KEY = 'test_secret_key'
    # A valid Fernet key for testing. Must be base64-encoded.
    ENCRYPTION_KEY = Fernet.generate_key().decode('utf-8')

@pytest.fixture(scope='session')
def app():
    app = create_app(TestConfig)
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture(scope='function')
def fernet_cipher(app):
    # Ensure the app context is active to get the ENCRYPTION_KEY
    with app.app_context():
        key = app.config['ENCRYPTION_KEY'].encode('utf-8')
        return Fernet(key)

# def test_encrypted_type_encryption_decryption(app, fernet_cipher):
#     # ... (test content) ...

def test_credencial_model_encryption(app, fernet_cipher):
    # ... (test content) ...

# def test_simple_credencial_insert(app):
#     # ... (test content) ...