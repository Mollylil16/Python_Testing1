import pytest
from server import app, competitions, clubs


def test_full_booking_flow(client):
    # Étape 1: Connexion avec un email valide
    login_response = client.post('/show_summary', data={'email': 'admin@irontemple.com'})
    assert login_response.status_code == 200
    assert b'Welcome' in login_response.data  # Cela peut rester tel quel car 'Welcome' est ASCII

    # Vérification de l’état initial des points et places
    club = next(c for c in clubs if c['name'] == 'Iron Temple')
    competition = next(c for c in competitions if c['name'] == 'Spring Festival')
    initial_points = int(club['points'])
    initial_places = int(competition['numberOfPlaces'])

    # Étape 2: Accéder à la page de réservation
    booking_page_response = client.get('/book/Spring Festival/Iron Temple')
    assert booking_page_response.status_code == 200

    # Étape 3: Réserver des places (4 places)
    booking_response = client.post(
        '/purchasePlaces',
        data={
            'competition': 'Spring Festival',
            'club': 'Iron Temple',
            'places': '4',
        },
    )
    assert booking_response.status_code == 200
    assert 'Super, réservation terminée !' in booking_response.data.decode('utf-8')  # Mis à jour

    # Étape 4: Vérification des mises à jour après la réservation
    updated_points = int(club['points'])
    updated_places = int(competition['numberOfPlaces'])

    assert updated_points == initial_points - 4  # 4 points en moins
    assert updated_places == initial_places - 4  # 4 places en moins

    # Étape 5: Vérification que les données sont toujours accessibles après réservation
    summary_response = client.post('/show_summary', data={'email': 'admin@irontemple.com'})
    assert summary_response.status_code == 200
    assert b'Iron Temple' in summary_response.data  # Cela peut rester tel quel
