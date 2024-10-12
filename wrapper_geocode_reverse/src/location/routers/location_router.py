import hashlib
from http import HTTPStatus
from typing import List

from fastapi import APIRouter, BackgroundTasks, Depends, Request, Response
from fastapi.responses import RedirectResponse
from geoalchemy2.functions import ST_GeogFromText
from pydantic import PositiveFloat, PositiveInt
from pydantic_extra_types.coordinate import Coordinate, Latitude, Longitude
from sqlalchemy.orm import Session

from wrapper_geocode_reverse.src.core import get_session, logger
from wrapper_geocode_reverse.src.core.cache import SimpleCache
from wrapper_geocode_reverse.src.core.measure import measure_time

from ..controllers.location_controller import (
    get_location_by_latitude_longitude,
    insert_locations,
)
from ..schemas.location_schema import Location, LocationServiceModel
from ..services.location_service import LocationService, get_service

TTL = 3600  # cache for 1 hour

location_router = APIRouter()

log = logger.getLogger(__name__)

cache = SimpleCache()


@measure_time
def search_cache(key: str, request: Request, response: Response):
    cached_locations = cache.get(key)

    if cached_locations:
        etag = hashlib.md5(str(cached_locations).encode()).hexdigest()
        logger.debug('Etag: %s', etag)

        if_none_match = request.headers.get('if_none_match', None)

        if if_none_match == etag:
            logger.debug('Not modified')
            response.status_code = HTTPStatus.NOT_MODIFIED

        response.headers['Cache-Control'] = f'public, max-age={TTL}'
        response.headers['ETag'] = etag

        logger.debug('Retrieved locations from cache')
        return cached_locations
    return None


@location_router.get('/', response_model=List[Location])
async def get_location_by_lat_long(
    lat: Latitude,
    long: Longitude,
    request: Request,
    response: Response,
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

    key = f'{point}{min_confidence}{number_points}{km_distance}'
    logger.debug('Cached key %s', key)

    location_cached = search_cache(key=key, request=request, response=response)

    if location_cached:
        return location_cached

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

        log.info('redirected request')
        url = 'get_location_by_lat_long_in_api'

        log.debug('redirected request to url %s', url)

        return RedirectResponse(
            request.url_for(url).include_query_params(**request.query_params),
            status_code=HTTPStatus.SEE_OTHER,
        )

    locations_db = [Location.model_validate(loc) for loc in locations]

    logger.info('Location cached for %s seconds', TTL)
    cache.set(key, locations_db, ttl=TTL)

    return locations_db


@location_router.get(
    '/api',
    include_in_schema=False,
)
async def get_location_by_lat_long_in_api(
    lat: Latitude,
    long: Longitude,
    background_tasks: BackgroundTasks,
    number_points: int = 1,
    min_confidence: PositiveFloat = 0.8,
    service: LocationService = Depends(get_service),
    session: Session = Depends(get_session),
):
    coordinate = Coordinate(lat, long)
    result_locations = await service.reverse_geocode(
        coordinate=coordinate,
        number_of_points=number_points,
    )

    background_tasks.add_task(
        insert_locations, session=session, locations=result_locations
    )

    locations_filtered = list(
        filter(
            lambda location: filter_locations_by_confidence(
                location, min_confidence
            ),
            result_locations,
        )
    )

    locations_by_api = [
        Location.model_validate(loc.model_dump()) for loc in locations_filtered
    ]

    return locations_by_api


def filter_locations_by_confidence(location: LocationServiceModel, confidence):
    return location.confidence >= confidence
