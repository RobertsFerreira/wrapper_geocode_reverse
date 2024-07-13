from http import HTTPStatus

from fastapi.testclient import TestClient

from wrapper_geocode_reverse.app import app


def test_root_and_return_running():
    client = TestClient(app)
    response = client.get('/v1/health')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'status': 'on'}
