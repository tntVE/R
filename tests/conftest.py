import pytest
from app import create_app, db
from config import Config

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:' # Use in-memory SQLite for tests
    # Ensure other critical variables are set for tests, even if dummy
    SECRET_KEY = 'test_secret_key'
    GOOGLE_CLIENT_ID = 'test_google_id'
    GOOGLE_CLIENT_SECRET = 'test_google_secret'
    ENCRYPTION_KEY = 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=' # Valid Fernet key for testing

@pytest.fixture(scope='session')
def app():
    app = create_app(TestConfig)
    with app.app_context():
        db.create_all() # Create tables for tests
        yield app
        db.session.remove()
        db.drop_all() # Drop tables after tests

@pytest.fixture(scope='function')
def client(app):
    return app.test_client()

@pytest.fixture(scope='function')
def runner(app):
    return app.test_cli_runner()
