import pytest
from app import app

@pytestfixture
def client():
    with app.test_client() as client:
        yield client

def test_public_club_points(client):
    response = client.get('/publicClubsPoints')
    assert response.status_code == 200
    assert b'Club Points' in response.data

def test_purchase_places(client):
    response = client.post('/purchasePlaces', data= {'competitions': 'Spring Festival', 'club': 'Simply Lift', 'place': '5'})
    assert response.status_code == 200
    assert b"Super, réservation terminée !" in response.data

def test_purchase_too_many_places(client):
    response = client.post('/purchasePlaces',  data= {'competitions': 'Spring Festival', 'club': 'Simply Lift', 'places': '15'})

assert response.status_code == 200
    assert b"Vous ne pouvez pas réserver plus de 12 places!" in response.data
