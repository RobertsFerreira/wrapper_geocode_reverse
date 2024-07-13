from fastapi import FastAPI
from wrapper_geocode_reverse.src.routers.router import base_router


app = FastAPI(version='0.0.1', summary='Location')


app.include_router(base_router)
