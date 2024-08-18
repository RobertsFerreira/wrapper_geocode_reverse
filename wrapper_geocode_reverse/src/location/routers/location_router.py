from http import HTTPStatus
from typing import List

from fastapi import APIRouter, BackgroundTasks, Depends, Request
from fastapi.responses import RedirectResponse
from geoalchemy2.functions import ST_GeogFromText
from pydantic import PositiveFloat, PositiveInt
from pydantic_extra_types.coordinate import Coordinate, Latitude, Longitude
from sqlalchemy.orm import Session

from wrapper_geocode_reverse.src.core import get_session
from wrapper_geocode_reverse.src.core.logger.logger import logger

from ..controllers.location_controller import (
    get_location_by_latitude_longitude,
    insert_locations,
)
from ..schemas.location_schema import Location
from ..services.location_service import LocationService, get_service

location_router = APIRouter()

log = logger.getLogger(__name__)


@location_router.get('/', response_model=List[Location])
async def get_location_by_lat_long(
    lat: Latitude,
    long: Longitude,
    request: Request,
    number_points: int = 1,
    min_confidence: PositiveFloat = 0.8,
    km_within: PositiveInt = 10,
    session: Session = Depends(get_session),
):
    coordinate = Coordinate(lat, long)

    km_distance = 1000 * km_within

    point = ST_GeogFromText(
        f'POINT({coordinate.latitude} {coordinate.longitude})', srid=4326
    )

    locations = get_location_by_latitude_longitude(
        session=session,
        point=point,
        min_confidence=min_confidence,
        number_points=number_points,
        km_distance=km_distance,
    )

    if not locations:
        msg = f'No locations found for coordinates ({coordinate.latitude}'
        msg = f'{msg} {coordinate.longitude}) within {km_within} km.'

        log.warning(msg)

        log.info(
            'redirect url to get_location_by_lat_long_in_api',
        )
        return RedirectResponse(
            request.url_for(
                'get_location_by_lat_long_in_api'
            ).include_query_params(**request.query_params),
            status_code=HTTPStatus.SEE_OTHER,
        )

    locations_db = [Location.model_validate(loc) for loc in locations]
    return locations_db


@location_router.get('/api')
async def get_location_by_lat_long_in_api(
    lat: Latitude,
    long: Longitude,
    background_tasks: BackgroundTasks,
    number_points: int = 1,
    service: LocationService = Depends(get_service),
    session: Session = Depends(get_session),
):
    coordinate = Coordinate(lat, long)
    result = await service.reverse_geocode(
        coordinate=coordinate,
        number_of_points=number_points,
    )

    background_tasks.add_task(
        insert_locations, session=session, locations=result
    )

    locations_by_api = [
        Location.model_validate(loc.model_dump()) for loc in result
    ]

    return locations_by_api
