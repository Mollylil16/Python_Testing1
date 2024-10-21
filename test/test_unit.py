from datetime import datetime
import sys
import os
from server import app
import server
from .config import client
import json

def load_clubs():
    with open('clubs.json') as c:
        return json.load(c)['clubs']

def load_competitions():
    with open('competitions.json') as comps:
        return json.load(comps)['competitions']


def test_index(client):
    response = client.get('/')
    assert response.status_code == 200
    assert 'Welcome to the GUDLFT Registration Portal!' in response.data.decode('utf-8')



def test_show_summary_with_valid_email(client):
    response = client.post(
        '/show_summary',
        data={'email': 'john@simplylift.co'},
    )
    assert response.status_code == 200
    assert 'Welcome' in response.data.decode('utf-8')

def test_show_summary_with_invalid_email(client):
    response = client.post(
        '/show_summary',
        data={'email': 'invalidemail@example.com'},
    )
    assert response.status_code == 302  # Redirection attendue

def test_show_summary_with_no_email(client):
    response = client.post(
        '/show_summary',
        data={'email': ''},
    )
    assert response.status_code == 302  # Redirection attendue

def test_purchase_places_valid(client):
    response = client.post(
        '/purchasePlaces',
        data={
            'competition': 'Spring Festival',
            'club': 'Simply Lift',
            'places': '5',
        },
    )
    assert response.status_code == 200
    assert 'Super, réservation terminée !' in response.data.decode('utf-8')

def test_purchase_places_insufficient_points(client):
    response = client.post(
        '/purchasePlaces',
        data={
            'competition': 'Spring Festival',
            'club': 'Iron Temple',
            'places': '10',
        },
    )
    assert response.status_code == 200
    assert 'Vous navez pas assez de points.' in response.data.decode('utf-8')
