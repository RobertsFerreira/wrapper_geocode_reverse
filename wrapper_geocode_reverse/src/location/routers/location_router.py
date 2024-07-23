from http import HTTPStatus
from typing import List

from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse
from geoalchemy2.functions import ST_DWithin, ST_GeogFromText
from pydantic import PositiveFloat, PositiveInt
from pydantic_extra_types.coordinate import Coordinate, Latitude, Longitude
from sqlalchemy import select
from sqlalchemy.orm import Session

from wrapper_geocode_reverse.src.core import get_session
from wrapper_geocode_reverse.src.location.schemas.location_schema import (
    Location,
)
from wrapper_geocode_reverse.src.location.services.location_service import (
    LocationService,
    get_service,
)
from wrapper_geocode_reverse.src.location.tables.location_table import (
    LocationTable,
)

location_router = APIRouter()


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
        f"POINT({coordinate.latitude} {coordinate.longitude})", srid=4326
    )

    locations = session.scalars(
        select(LocationTable)
        .where(
            ST_DWithin(LocationTable.latitude_longitude, point, km_distance)
        )
        .where(LocationTable.confidence >= min_confidence)
        .limit(number_points)
        .order_by(LocationTable.confidence.desc()),
    ).all()

    if not locations:
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
    number_points: int = 1,
    service: LocationService = Depends(get_service),
):
    coordinate = Coordinate(lat, long)
    result = await service.reverse_geocode(
        coordinate=coordinate,
        number_of_points=number_points,
    )

    locations_by_api = [
        Location.model_validate(loc.model_dump()) for loc in result
    ]

    return locations_by_api
