from http import HTTPStatus
from typing import Any, List

from fastapi import Depends
from httpx import AsyncClient

from wrapper_geocode_reverse.src.core.settings.settings import Settings
from wrapper_geocode_reverse.src.location.schemas.location_schema import (
    LocationServiceModel,
)


class LocationService:
    settings: Settings

    BASE_URL_SERVICE: str
    API_KEY: str

    def __init__(self, settings=Depends(Settings())):  # type: ignore
        self.settings = settings
        self.BASE_URL_SERVICE = self.settings.OPEN_ROUTER_GEOCODE_REVERSE_URL
        self.API_KEY = self.settings.OPEN_ROUTER_TOKEN

    async def reverse_geocode(self, latitude: str, longitude: str):
        params = {
            'api_key': self.API_KEY,
            'point.lon': longitude,
            'point.lat': latitude,
        }

        async with AsyncClient(base_url=self.BASE_URL_SERVICE) as client:
            response = await client.get(
                '/geocode/reverse',
                params=params,
            )
            if response.status_code != HTTPStatus.OK:
                raise Exception(
                    f'Error fetching data from OpenRouter API: {
                        response.status_code
                    }'
                )
            open_router_response: dict[str, Any] = response.json()
            if 'features' in open_router_response.keys():
                features: List[dict[str, Any]] = open_router_response[
                    'features'
                ]
                locations = [
                    LocationServiceModel.model_validate(feature)
                    for feature in features
                ]
                return locations[0].city
