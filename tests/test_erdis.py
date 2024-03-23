from pathlib import Path

# get the resources folder in the tests folder
resources = Path(__file__).parent / "resources"


def test_request_example(client):
    response = client.get('/hello')

    assert b'Hello, World!' in response.data

def test_assegnazioni(client):
    response = client.post('/', data={
        "name": "Flask",
        "theme": "dark",
    })

    assert response.status_code == 200