from http import HTTPStatus

import pytest
import respx
from httpx import Response

from tests.src.utils.data.fake_data import fake_location
from wrapper_geocode_reverse.src.core.settings.settings import (
    Settings,
    get_settings,
)
from wrapper_geocode_reverse.src.location.service.location_service import (
    LocationService,
)

settings = Settings()  # type: ignore

Size_OF_CITIES_RETURNED = 1
CITY_FOR_TEST = 'Tocantins'


@pytest.mark.asyncio()
async def test_must_return_city_by_latitude_and_longitude():
    params = {
        'api_key': settings.OPEN_ROUTER_TOKEN,
        'point.lon': '2.294471',
        'point.lat': '48.858268',
        'size': Size_OF_CITIES_RETURNED,
    }

    with respx.mock(
        base_url=settings.OPEN_ROUTER_GEOCODE_REVERSE_URL
    ) as respx_mock:
        location_mock = respx_mock.get('/geocode/reverse', params=params)
        location_mock.return_value = Response(
            HTTPStatus.OK, json=fake_location
        )

        location_service = LocationService(get_settings())

        locations = await location_service.reverse_geocode(
            longitude='2.294471', latitude='48.858268'
        )

        location = locations[0]

        assert location.city == CITY_FOR_TEST


@pytest.mark.asyncio()
async def test_must_return_quantity_city_of_params_size():
    latitude = '-21.174267'
    longitude = '-43.024593'
    params = {
        'api_key': settings.OPEN_ROUTER_TOKEN,
        'point.lon': longitude,
        'point.lat': latitude,
        'size': 1,
    }

    with respx.mock(
        base_url=settings.OPEN_ROUTER_GEOCODE_REVERSE_URL
    ) as respx_mock:
        location_mock = respx_mock.get('/geocode/reverse', params=params)
        location_mock.return_value = Response(
            HTTPStatus.OK, json=fake_location
        )

        location_service = LocationService(get_settings())

        cities = await location_service.reverse_geocode(
            longitude=longitude,
            latitude=latitude,
        )

        assert len(cities) == Size_OF_CITIES_RETURNED
