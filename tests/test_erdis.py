from pathlib import Path

# get the resources folder in the tests folder
resources = Path(__file__).parent / "resources"


def test_request_example(client):
    response = client.get('/hello')

    assert b'Hello, World!' in response.data


def test_home(client):
    response = client.get('/')

    assert response.status.code == 200


def test_assegnazioni(client):
    response = client.post('/assegnazioni', data={
        "name": "Flask",
        "theme": "dark",
    })

    assert response.status_code == 302
