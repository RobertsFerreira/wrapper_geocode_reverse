from http import HTTPStatus

from fastapi.testclient import TestClient
from pydantic_extra_types.coordinate import Coordinate


def test_get_location_by_coordinates(
    client: TestClient,
    coordinate: Coordinate,
):
    response = client.get(
        '/v1/location/api',
        params={
            'lat': coordinate.latitude,
            'long': coordinate.longitude,
        },
    )

    assert response.status_code == HTTPStatus.OK


def test_get_location_by_coordinates_on_bd(
    client: TestClient,
    coordinate: Coordinate,
):
    response = client.get(
        '/v1/location',
        params={
            'lat': coordinate.latitude,
            'long': coordinate.longitude,
        },
    )

    location = response.json()[0]

    lat = location['latitude']
    long = location['longitude']

    assert response.status_code == HTTPStatus.OK
    assert coordinate.latitude == lat
    assert coordinate.longitude == long
