import json
import pytest
from server import app

@pytest.fixture
def client():
    app.testing = True
    with app.test_client() as client:
        yield client

def test_index_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"Welcome to the GUDLFT Registration Portal!" in response.data

def test_view_public_club_points(client):
    response = client.get('/publicClubPoints')
    assert response.status_code == 200
    assert b"Club Points" in response.data

def test_booking_page(client):
    # Simule l'accès à la page de réservation après avoir soumis l'email
    client.post('/showSummary', data={'email': 'john@simplylift.co'})
    response = client.get('/book/Spring Festival/Simply Lift')
    assert response.status_code == 200
    assert b"How many places?" in response.data

def test_invalid_email_submission(client):
    response = client.post('/showSummary', data={'email': 'invalid_email'})
    assert response.status_code == 302  # Redirection vers la page d'accueil
    assert b"Format d'email invalide, veuillez réessayer." in response.data

def test_not_found_email(client):
    response = client.post('/showSummary', data={'email': 'unknown@club.com'})
    assert response.status_code == 302  # Redirection vers la page d'accueil
    assert b"Email non trouvé, veuillez réessayer." in response.data
