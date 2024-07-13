from fastapi import APIRouter, Depends
from pydantic_extra_types.coordinate import Coordinate, Latitude, Longitude

from wrapper_geocode_reverse.src.location.services.location_service import (
    LocationService,
    get_service,
)

location_router = APIRouter()


@location_router.get('/')
async def get_location_by_lat_long(
    lat: Latitude,
    lon: Longitude,
    service: LocationService = Depends(get_service),
):
    coordinate = Coordinate(lat, lon)
    result = await service.reverse_geocode(coordinate=coordinate)
    return result
