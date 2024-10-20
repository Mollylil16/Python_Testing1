from server import app 
import pytest

@pytest.fixture
def client():
    app.testing = True
    with app.test_client() as client:
        yield client 