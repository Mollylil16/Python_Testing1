import json
import pytest
from server import app

@pytest.fixture
def client():
    app.testing = True
    with app.test_client() as client:
        yield client

def test_show_summary(client):
    response = client.post('/showSummary', data={'email': 'john@simplylift.co'})
    assert b"Welcome, john@simplylift.co" in response.data
    assert response.status_code == 200

def test_book_places_integration(client):
    # Simule une réservation avec des données valides
    client.post('/showSummary', data={'email': 'john@simplylift.co'})
    response = client.post('/purchasePlaces', data={
        'club': 'Simply Lift',
        'competition': 'Spring Festival',
        'places': '2'
    })
    assert b"Super, réservation terminée !" in response.data

def test_insufficient_places(client):
    # Teste une réservation dépassant le nombre de places disponibles
    client.post('/showSummary', data={'email': 'john@simplylift.co'})
    response = client.post('/purchasePlaces', data={
        'club': 'Simply Lift',
        'competition': 'Spring Festival',
        'places': '30'  # Plus que le disponible
    })
    assert b"Pas assez de places disponibles pour ce concours." in response.data

def test_logout(client):
    response = client.get('/logout')
    assert response.status_code == 302  # Redirige vers la page d'accueil
    assert response.location == "http://localhost/"
