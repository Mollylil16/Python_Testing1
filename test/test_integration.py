import pytest
from server import app
from .config import client




def test_reservation_updates_points_and_availability(client):
    response = client.post('/purchasePlaces', data={'competition': 'Spring Festival', 'club': 'Iron Temple', 'places': '2'})
    assert response.status_code == 200
    assert 'Great - booking complete!' in response.data.decode('utf-8')

    summary_response = client.post('/showSummary', data={'email': 'admin@irontemple.com'})
    assert summary_response.status_code == 200
    assert b'Iron Temple' in summary_response.data

    booking_page_response = client.get('/book/Spring Festival/Iron Temple')
    assert booking_page_response.status_code == 200
    assert b'Available Places' in booking_page_response.data