import pytest
from app.server import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_book(client):
    response = client.get('/book/Spring Festival/Simply Lift')
    assert response.status_code == 200
    assert b'Booking for Spring Festival' in response.data  

def test_purchase_places(client):
    # Créer un club dans la session pour tester l'achat de places
    client.post('/showSummary', data={'email': 'john@simplylift.co'})
    
    response = client.post('/purchasePlaces', data={
        'competition': 'Spring Festival',
        'club': 'Simply Lift',
        'places': '3'
    })
    assert response.status_code == 200
    
    # Changez cette ligne pour décoder la réponse en UTF-8
    assert b'Super, réservation terminée!' in response.data
