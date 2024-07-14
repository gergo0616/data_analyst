import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"Restaurant Analyzer" in response.data

def test_results_page(client):
    response = client.post('/', data={'location': 'New York'})
    assert response.status_code == 200
    assert b"Analysis Results" in response.data