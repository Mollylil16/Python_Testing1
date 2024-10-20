import pytest
from server import app
from .config import client

@pytest.fixture
def client():
    app.testing = True
    with app.test_client() as client:
        yield client

def test_show_summary(client):
    response = client.post('/showSummary', data={'email': 'john@simplylift.co'})
    assert response.status_code == 200
    assert b"Welcome" in response.data

def test_purchase_places(client):
    response = client.post('/purchasePlaces', data={
        'club': 'ClubTest',
        'competition': 'CompetitionTest',
        'places': 5
    })
    assert response.status_code == 200
    assert "Super, réservation terminée !".encode('utf-8') in response.data
