import pytest
from app import create_app, db
from config import Config

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SECRET_KEY = 'test_secret_key'
    GOOGLE_CLIENT_ID = 'test_google_id'
    GOOGLE_CLIENT_SECRET = 'test_google_secret'
    ENCRYPTION_KEY = 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA='

@pytest.fixture(scope='session')
def app():
    app = create_app(TestConfig)
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture(scope='function')
def client(app):
    return app.test_client()

def test_programming_home_page(client):
    """Test the programming home page loads correctly"""
    response = client.get('/programming/')
    assert response.status_code == 200
    assert b'Aprender a Programar' in response.data
    assert b'Conceptos B\xc3\xa1sicos de Programaci\xc3\xb3n' in response.data
    assert b'Introducci\xc3\xb3n a Python' in response.data

def test_conceptos_basicos_page(client):
    """Test the basic concepts page loads correctly"""
    response = client.get('/programming/conceptos-basicos')
    assert response.status_code == 200
    assert b'Conceptos B\xc3\xa1sicos de Programaci\xc3\xb3n' in response.data
    assert b'\xc2\xbfQu\xc3\xa9 es la Programaci\xc3\xb3n?' in response.data
    assert b'Variables' in response.data

def test_python_introduction_page(client):
    """Test the Python introduction page loads correctly"""
    response = client.get('/programming/python-introduccion')
    assert response.status_code == 200
    assert b'Introducci\xc3\xb3n a Python' in response.data
    assert b'print(' in response.data

def test_estructuras_control_page(client):
    """Test the control structures page loads correctly"""
    response = client.get('/programming/estructuras-control')
    assert response.status_code == 200
    assert b'Estructuras de Control' in response.data
    assert b'if edad' in response.data

def test_funciones_page(client):
    """Test the functions page loads correctly"""
    response = client.get('/programming/funciones')
    assert response.status_code == 200
    assert b'Funciones' in response.data
    assert b'def saludar' in response.data

def test_ejercicios_page(client):
    """Test the exercises page loads correctly"""
    response = client.get('/programming/ejercicios')
    assert response.status_code == 200
    assert b'Ejercicios Pr\xc3\xa1cticos' in response.data
    assert b'Saludo Personalizado' in response.data

def test_recursos_page(client):
    """Test the resources page loads correctly"""
    response = client.get('/programming/recursos')
    assert response.status_code == 200
    assert b'Recursos Adicionales' in response.data
    assert b'Consejos para Seguir Aprendiendo' in response.data

def test_main_page_contains_programming_link(client):
    """Test that the main page contains a link to programming section"""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Aprender a Programar' in response.data
    assert b'/programming/' in response.data