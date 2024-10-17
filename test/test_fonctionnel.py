import pytest
from server import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_public_club_points(client):
    response = client.get('/publicClubsPoints')
    assert response.status_code == 200
    assert b'Club Points' in response.data.decode('utf-8')

def test_purchase_places(client):
    response = client.post('/purchasePlaces', data= {'competition': 'Spring Festival', 'club': 'Simply Lift', 'places': '5'})
    assert response.status_code == 200
    assert "Super, réservation terminée !" in response.data.decode('utf-8')

def test_purchase_too_many_places(client):
    response = client.post('/purchasePlaces',  data= {'competition': 'Spring Festival', 'club': 'Simply Lift', 'places': '15'})
    assert response.status_code == 200
    assert "Vous ne pouvez pas réserver plus de 12 places!" in response.data.decode('utf-8')