import json
import pytest
from server import app, loadClubs, loadCompetitions

@pytest.fixture
def client():
    app.testing = True
    with app.test_client() as client:
        yield client

def test_load_clubs():
    clubs = loadClubs()
    assert isinstance(clubs, list)  # Doit retourner une liste
    assert len(clubs) > 0  # Vérifie qu'il y a au moins un club

def test_load_competitions():
    competitions = loadCompetitions()
    assert isinstance(competitions, list)  # Doit retourner une liste
    assert len(competitions) > 0  # Vérifie qu'il y a au moins une compétition

def test_email_format_validation(client):
    response = client.post('/showSummary', data={'email': 'invalid-email'})
    assert b"Format d'email invalide, veuillez réessayer." in response.data

def test_valid_email(client):
    response = client.post('/showSummary', data={'email': 'john@simplylift.co'})
    assert b"Welcome, john@simplylift.co" in response.data

def test_book_places(client):
    # Simulation d'une réservation avec des données valides
    client.post('/showSummary', data={'email': 'john@simplylift.co'})
    response = client.post('/purchasePlaces', data={
        'club': 'Simply Lift',
        'competition': 'Spring Festival',
        'places': '2'
    })
    assert b"Super, réservation terminée !" in response.data

def test_insufficient_points(client):
    # Simule une situation où les points ne suffisent pas
    client.post('/showSummary', data={'email': 'admin@irontemple.com'})
    response = client.post('/purchasePlaces', data={
        'club': 'Iron Temple',
        'competition': 'Fall Classic',
        'places': '5'
    })
    assert b"Vous n'avez pas assez de points." in response.data

def test_index_page(client):
    response = client.get('/')
    assert b"Welcome to the GUDLFT Registration Portal!" in response.data
    assert response.status_code == 200

def test_points_page(client):
    response = client.get('/publicClubPoints')
    assert b"Club Points" in response.data
    assert response.status_code == 200
