import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'biblioteca_python'))

from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_check(client):
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json['status'] == 'ok'

def test_index_page(client):
    response = client.get('/')
    assert response.status_code == 200

def test_login_empty_credentials(client):
    response = client.post('/Usuarios/validar', data={'usuario': '', 'clave': ''})
    assert response.status_code == 400

def test_login_missing_credentials(client):
    response = client.post('/Usuarios/validar', data={})
    assert response.status_code == 400
