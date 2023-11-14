import pytest
from server import app
from flask import get_flashed_messages

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            yield client

#bug1:ERROR: Entering a unknown email crashes the app
def test_unknown_email(client):
    response = client.post('/showSummary', data={'email': 'test@test.com'}, follow_redirects=True)
    assert response.status_code == 404
    assert b"Sorry, that email wasn't found." in response.data

#bug2:BUG: Clubs should not be able to use more than their points allowed
def test_purchase_over_points(client):
    response = client.post('/purchasePlaces', data={
        'club': 'Iron Temple',
        'competition': 'Fall Classic',
        'places': '10'
    }, follow_redirects=True)
    flashed_messages = get_flashed_messages()
    assert "You don't have enough points to book 10 places." in flashed_messages

#bug3:BUG: Clubs shouldn't be able to book more than 12 places per competition #4
def test_booking_limit_exceeded(client):
    response = client.post('/purchasePlaces', data={
        'club': 'Iron Temple',
        'competition': 'Fall Classic',
        'places': '13'
    }, follow_redirects=True)
    flashed_messages = get_flashed_messages()
    assert "You cannot book more than 12 places." in flashed_messages

# bug4:BUG: Booking places in past competitions should not be allowed
def test_booking_in_past_competition(client):
    response = client.get('/book/Spring Festival/Iron Temple', follow_redirects=True)
    flashed_messages = get_flashed_messages()
    assert "This competition has already passed." in flashed_messages