import pytest
import json
from server import app

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

def test_insufficient_points_and_past_competition(client):
    # Attempt to register with 15 points
    response = client.post('/purchasePlaces', data={
        'club': 'Simply Lift',
        'competition': 'Fall Classic',
        'places': '15'
    }, follow_redirects=True)
    assert b"You cannot book more than 12 places." in response.data

    # Attempt to enter a past competition
    response = client.get('/book/Spring Festival/Simply Lift', follow_redirects=True)
    assert b"This competition has already passed." in response.data

def test_points_deduction_after_booking(client):
    # Loading club data before booking
    initial_points = 12  # Initial points of 'She Lifts

    # Register for a competition
    client.post('/purchasePlaces', data={
        'club': 'She Lifts',
        'competition': 'Tournoi Test',
        'places': '1'
    }, follow_redirects=True)

    # Checking points after booking
    response = client.post('/showSummary', data={'email': 'kate@shelifts.co.uk'}, follow_redirects=True)
    updated_club_data = response.data.decode()
    expected_points = initial_points - 1
    assert str(expected_points) in updated_club_data


