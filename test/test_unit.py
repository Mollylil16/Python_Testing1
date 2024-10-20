import sys
import os
from server import app
from .config import client

sys.path.insert(
    0,
    os.path.join(os.path.dirname(__file__), '..'),
)

def test_index(client):
    response = client.get('/')
    assert response.status_code == 200
