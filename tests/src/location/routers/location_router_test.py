from http import HTTPStatus

from fastapi.testclient import TestClient
from pydantic_extra_types.coordinate import Coordinate


def test_get_location_by_coordinates(
        client: TestClient,
        coordinate: Coordinate,
):
    response = client.get(
        '/v1/location',
        params={
            'lat': coordinate.latitude,
            'long': coordinate.longitude,
        }
    )

    assert response.status_code == HTTPStatus.OK
