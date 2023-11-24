import pytest
import json
from server import app, loadClubs, loadCompetitions

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_page_navigation(client):
    # Test accessing the home page
    response = client.get('/')
    assert response.status_code == 200

    # Test accessing the points page
    response = client.get('/points')
    assert response.status_code == 200

    # Test redirecting to home page
    response = client.get('/logout', follow_redirects=True)
    assert b'Welcome to the GUDLFT Registration Portal!' in response.data
