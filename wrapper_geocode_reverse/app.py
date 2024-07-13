from fastapi import APIRouter, FastAPI

from wrapper_geocode_reverse.src.location.routers.location_router import (
    location_router,
)

app = FastAPI(version='0.0.1', summary='Location')

base_router = APIRouter(prefix='/v1')

app.include_router(base_router)

base_router.include_router(
    location_router, prefix='/location', tags=['location']
)


@base_router.get('/')
def root():
    return {'status': 'on'}
