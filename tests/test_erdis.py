def test_request_example(client):
    response = client.get('/hello')

    assert b'Hello, World!' in response.data
