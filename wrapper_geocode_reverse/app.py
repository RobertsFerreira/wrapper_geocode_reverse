from fastapi import FastAPI

from wrapper_geocode_reverse.src.core import logger
from wrapper_geocode_reverse.src.routers.router import base_router

logger.getLogger('watchfiles.main').setLevel(logger.CRITICAL)

app = FastAPI(version='0.0.1', summary='Location')

app.include_router(base_router)
