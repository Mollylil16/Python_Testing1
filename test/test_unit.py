import json
import pytest
from app.server import loadClubs, loadCompetitions

def test_load_clubs():
    clubs = loadClubs()
    assert isinstance(clubs, list)
    assert len(clubs) > 0
    assert "name" in clubs[0]
    assert "email" in clubs[0]
    assert "points" in clubs[0]

def test_load_competitions():
    competitions = loadCompetitions()
    assert isinstance(competitions, list)
    assert len(competitions) > 0
    assert "name" in competitions[0]
    assert "date" in competitions[0]
    assert "numberOfPlaces" in competitions[0]
