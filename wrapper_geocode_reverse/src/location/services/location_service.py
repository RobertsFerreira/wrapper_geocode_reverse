from http import HTTPStatus
from typing import Any, List

from httpx import AsyncClient
from pydantic_extra_types.coordinate import Coordinate

from wrapper_geocode_reverse.src.core.logger.logger import logger
from wrapper_geocode_reverse.src.core.settings.settings import (
    Settings,
)
from wrapper_geocode_reverse.src.location.schemas.location_schema import (
    LocationServiceModel,
)


class LocationService:
    settings: Settings

    BASE_URL_SERVICE: str
    API_KEY: str

    def __init__(self, settings: Settings):  # type: ignore
        self.settings = settings
        self.BASE_URL_SERVICE = self.settings.OPEN_ROUTER_GEOCODE_REVERSE_URL
        self.API_KEY = self.settings.OPEN_ROUTER_TOKEN
        self.logger = logger.getLogger(__name__)

    async def reverse_geocode(
        self,
        coordinate: Coordinate,
        number_of_points: int = 1,
    ) -> list[LocationServiceModel]:
        params = {
            'api_key': self.API_KEY,
            'point.lon': coordinate.longitude,
            'point.lat': coordinate.latitude,
            'size': number_of_points,
        }

        locations: list[LocationServiceModel] = []

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
            if 'features' not in open_router_response.keys():
                self.logger.error('Error get features from OpenRouter')
            features: List[dict[str, Any]] = open_router_response['features']
            for feature in features:
                if 'properties' not in feature.keys():
                    raise Exception('Error get proprieties of location')
                propriety_location = feature.get('properties')

                location = LocationServiceModel.model_validate(
                    propriety_location
                )

                geometry = feature.get('geometry')
                if geometry is None:
                    raise Exception('Error get geometry of location')
                location_coordinates = geometry.get('coordinates')
                if not location_coordinates:
                    raise Exception('Error get coordinates of location')

                location = location.model_copy(
                    update={
                        'longitude': location_coordinates[0],
                        'latitude': location_coordinates[1],
                    }
                )

                locations.append(location)
            return locations


def get_service():
    return LocationService(Settings())  # type: ignore
