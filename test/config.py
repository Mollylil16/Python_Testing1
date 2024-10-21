from server import app 
import pytest

@pytest.fixture
def client():
    app.testing = True  # cette ligne mets l'application flask en mode test
    with app.test_client() as client:  # cela crée un client pour l'application flask permettant la simulation des requêtes
        yield client  # permet à la fixture de retourner le client test
