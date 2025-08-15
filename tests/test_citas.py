import pytest
from unittest.mock import MagicMock, patch
from app import create_app, db
from app.models.credencial import Credencial
from app.models.user import User
from app.services import gcalendar_service
from config import Config
import datetime
import pytz

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:' # Use in-memory SQLite for tests
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

@pytest.fixture(scope='function')
def new_user(app):
    with app.app_context():
        user = User(email='test@example.com', role='doctor', timezone='America/Santiago')
        user.set_password('password')
        db.session.add(user)
        db.session.commit()
        yield user
        db.session.delete(user)
        db.session.commit()

@pytest.fixture(scope='function')
def user_credentials(app, new_user):
    with app.app_context():
        creds = Credencial(
            user_id=new_user.id,
            token='test_token',
            refresh_token='test_refresh_token',
            token_uri='https://oauth2.googleapis.com/token',
            scopes='https://www.googleapis.com/auth/calendar.events'
        )
        db.session.add(creds)
        db.session.commit()
        yield creds
        db.session.delete(creds)
        db.session.commit()

# --- Tests for gcalendar_service.py --- 

def test_build_gcal_service_no_credentials(app, new_user):
    with app.app_context():
        service = gcalendar_service.build_gcal_service(user_id=new_user.id)
        assert service is None

@patch('googleapiclient.discovery.build')
@patch('google.oauth2.credentials.Credentials')
def test_build_gcal_service_with_credentials(mock_credentials, mock_build, app, new_user, user_credentials):
    with app.app_context():
        # Mock the Credentials object behavior
        mock_credentials_instance = MagicMock()
        mock_credentials_instance.expired = False
        mock_credentials_instance.refresh_token = 'test_refresh_token'
        mock_credentials_instance.token = 'test_token'
        mock_credentials_instance.token_uri = 'https://oauth2.googleapis.com/token'
        mock_credentials_instance.scopes = ['https://www.googleapis.com/auth/calendar.events']
        mock_credentials.return_value = mock_credentials_instance

        # Mock the build function
        mock_build.return_value = MagicMock()

        service = gcalendar_service.build_gcal_service(user_id=new_user.id)
        assert service is not None
        mock_build.assert_called_once_with('calendar', 'v3', credentials=mock_credentials_instance)

@patch('googleapiclient.discovery.build')
@patch('google.oauth2.credentials.Credentials')
def test_build_gcal_service_token_refresh(mock_credentials, mock_build, app, new_user, user_credentials):
    with app.app_context():
        # Mock the Credentials object behavior for expired token
        mock_credentials_instance = MagicMock()
        mock_credentials_instance.expired = True
        mock_credentials_instance.refresh_token = 'old_refresh_token'
        mock_credentials_instance.token = 'old_token'
        mock_credentials_instance.token_uri = 'https://oauth2.googleapis.com/token'
        mock_credentials_instance.scopes = ['https://www.googleapis.com/auth/calendar.events']
        mock_credentials.return_value = mock_credentials_instance

        # Mock the Flow.from_client_config and its oauth2session.refresh_token
        with patch('google_auth_oauthlib.flow.Flow.from_client_config') as mock_flow_from_client_config:
            mock_flow_instance = MagicMock()
            mock_flow_from_client_config.return_value = mock_flow_instance
            mock_flow_instance.oauth2session.refresh_token.return_value = None # Simulate successful refresh
            mock_flow_instance.credentials = MagicMock(token='new_token', refresh_token='new_refresh_token') # New credentials after refresh

            service = gcalendar_service.build_gcal_service(user_id=new_user.id)
            assert service is not None
            mock_flow_instance.oauth2session.refresh_token.assert_called_once()
            assert user_credentials.token == 'new_token'
            assert user_credentials.refresh_token == 'new_refresh_token'

@patch('app.services.gcalendar_service.build_gcal_service')
def test_find_available_slots(mock_build_service, app, new_user):
    with app.app_context():
        mock_service = MagicMock()
        mock_build_service.return_value = mock_service

        # Mock the freebusy.query method
        mock_service.freebusy().query().execute.return_value = {
            'calendars': {
                'primary': {
                    'busy': [
                        {'start': '2025-08-15T10:00:00-04:00', 'end': '2025-08-15T11:00:00-04:00'},
                        {'start': '2025-08-15T14:30:00-04:00', 'end': '2025-08-15T15:00:00-04:00'}
                    ]
                }
            }
        }

        # Set a specific date for testing
        test_date = datetime.date(2025, 8, 15)
        
        available_slots = gcalendar_service.find_available_slots(mock_service, day=test_date)
        
        # Expected available slots for 9:00-17:00 with 10:00-11:00 and 14:30-15:00 busy
        # Assuming Santiago timezone is -04:00 for simplicity in test
        expected_slots = [
            {'start': '2025-08-15T09:00:00-04:00', 'end': '2025-08-15T10:00:00-04:00'},
            {'start': '2025-08-15T11:00:00-04:00', 'end': '2025-08-15T12:00:00-04:00'},
            {'start': '2025-08-15T12:00:00-04:00', 'end': '2025-08-15T13:00:00-04:00'},
            {'start': '2025-08-15T13:00:00-04:00', 'end': '2025-08-15T14:00:00-04:00'},
            {'start': '2025-08-15T15:00:00-04:00', 'end': '2025-08-15T16:00:00-04:00'},
            {'start': '2025-08-15T16:00:00-04:00', 'end': '2025-08-15T17:00:00-04:00'}
        ]
        
        # Convert expected slots to the same timezone as the function output
        santiago_tz = pytz.timezone('America/Santiago')
        for slot in expected_slots:
            start_dt = datetime.datetime.fromisoformat(slot['start']).astimezone(santiago_tz)
            end_dt = datetime.datetime.fromisoformat(slot['end']).astimezone(santiago_tz)
            slot['start'] = start_dt.isoformat()
            slot['end'] = end_dt.isoformat()

        assert available_slots == expected_slots

@patch('app.services.gcalendar_service.build_gcal_service')
def test_create_calendar_event(mock_build_service, app, new_user):
    with app.app_context():
        mock_service = MagicMock()
        mock_build_service.return_value = mock_service

        # Mock the events().insert().execute() method
        mock_service.events().insert().execute.return_value = {'htmlLink': 'http://mocklink.com'}

        # Define test data
        santiago_tz = pytz.timezone('America/Santiago')
        start_time = datetime.datetime(2025, 8, 15, 10, 0, 0).astimezone(santiago_tz)
        end_time = datetime.datetime(2025, 8, 15, 11, 0, 0).astimezone(santiago_tz)
        attendees = ['attendee@example.com']

        event_link = gcalendar_service.create_calendar_event(
            mock_service, 'primary', 'Test Summary', 'Test Description',
            start_time, end_time, attendees
        )

        assert event_link == 'http://mocklink.com'
        mock_service.events().insert().execute.assert_called_once()

# --- Integration Tests for Auth Routes ---

def test_register_user(client, app):
    with app.app_context():
        response = client.post('/auth/register', data={
            'email': 'newuser@example.com',
            'password': 'newpassword',
            'role': 'doctor', # Default role
            'timezone': 'America/Santiago' # Default timezone
        })
        assert response.status_code == 200 # Should redirect or show success message
        assert b'Registro exitoso' in response.data # Check for flash message

        user = User.query.filter_by(email='newuser@example.com').first()
        assert user is not None
        assert user.check_password('newpassword')

def test_register_existing_user(client, app, new_user):
    with app.app_context():
        response = client.post('/auth/register', data={
            'email': new_user.email,
            'password': 'anotherpassword'
        })
        assert response.status_code == 200
        assert b'Ese email ya est' in response.data # Check for flash message

def test_login_user(client, app, new_user):
    with app.app_context():
        response = client.post('/auth/login', data={
            'email': new_user.email,
            'password': 'password'
        })
        assert response.status_code == 302 # Should redirect on successful login
        assert response.headers['Location'] == '/main/index' # Assuming this redirect

def test_login_invalid_credentials(client, app, new_user):
    with app.app_context():
        response = client.post('/auth/login', data={
            'email': new_user.email,
            'password': 'wrongpassword'
        })
        assert response.status_code == 200 # Should render login page with error
        assert b'Email o contrase' in response.data # Check for flash message

def test_logout_user(client, app, new_user):
    with app.app_context():
        # First, log in the user
        client.post('/auth/login', data={
            'email': new_user.email,
            'password': 'password'
        })
        
        # Then, log out
        response = client.get('/auth/logout')
        assert response.status_code == 302 # Should redirect
        assert response.headers['Location'] == '/auth/login'

# --- Integration Tests for Protected API Endpoints ---

def test_list_calendars_requires_login(client):
    response = client.get('/auth/list_calendars')
    assert response.status_code == 302 # Redirect to login

def test_book_appointment_requires_login(client):
    response = client.post('/auth/book_appointment', json={})
    assert response.status_code == 302 # Redirect to login
