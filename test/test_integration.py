import pytest
from app.server import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_index(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Welcome' in response.data  # Vérifiez que la page d'accueil contient un élément spécifique

def test_show_summary(client):
    response = client.post('/showSummary', data={'email': 'john@simplylift.co'})
    assert response.status_code == 200
    assert b'Welcome, Simply Lift!' in response.data

def test_show_summary_invalid_email(client):
    response = client.post('/showSummary', data={'email': 'invalid_email'})
    assert response.status_code == 302  # Redirection après une erreur
    assert b'Format d\'email invalide' in response.data
