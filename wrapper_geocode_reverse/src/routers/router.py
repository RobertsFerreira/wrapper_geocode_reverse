from fastapi import APIRouter

from wrapper_geocode_reverse.src.location.routers.location_router import (
    location_router,
)

base_router = APIRouter(prefix='/v1')


base_router.include_router(
    location_router, prefix='/location', tags=['location']
)


@base_router.get('/health')
def root():
    return {'status': 'on'}
