import sys
import os
from server import app
from .config import client


sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..'),
    ),
)

def test_full_booking_flow(client):
    login_response = client.post('/show_summary', data={'email': 'john@simplylift.co'})
    assert login_response.status_code == 200

    booking_page_response = client.get('/book/Spring Festival/Simply Lift')
    assert booking_page_response.status_code == 200

    booking_response = client.post(
        '/purchasePlaces',
        data={
            'competition': 'Spring Festival',
            'club': 'Simply Lift',
            'places': '8',
        },
    )
    assert booking_response.status_code == 200
    assert 'Super, réservation terminée !' in booking_response.data.decode('utf-8')

    summary_response = client.post('/show_summary', data={'email': 'john@simplylift.co'})
    assert summary_response.status_code == 200
    assert b'Simply Lift' in summary_response.data

    booking_page_response_after = client.get('/book/Spring Festival/Simply Lift')
    assert booking_page_response_after.status_code == 200
    assert b'Available Places' in booking_page_response_after.data