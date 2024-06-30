import os

import pytest
from fastapi.testclient import TestClient
from geoalchemy2 import load_spatialite
from sqlalchemy import create_engine, select
from sqlalchemy.event import listen
from sqlalchemy.orm import Session

from wrapper_geocode_reverse.app import app
from wrapper_geocode_reverse.src.location.tables.location_table import (
    LocationTable,
    table_registry,
)


@pytest.fixture()
def client():
    return TestClient(app)


@pytest.fixture()
def session():
    engine = create_engine('sqlite:///:memory:')

    base_path = 'E:\\ProjetosPY\\wrapper_geocode_reverse'
    path = f'{base_path}\\plugins\\spatialite\\mod_spatialite.dll'

    os.environ['SPATIALITE_LIBRARY_PATH'] = path

    listen(engine, 'connect', load_spatialite)
    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    table_registry.metadata.drop_all(engine)


@pytest.fixture()
def fixture_location_create(session):
    latitude, longitude = 1, 1
    point = f'POINT({latitude} {longitude})'
    new_location = LocationTable(
        address='address',
        latitude=1.0,
        longitude=1.0,
        city='city',
        state='state',
        country='country',
        postal_code='postal_code',
        latitude_longitude=point,  # type: ignore
    )

    session.add(new_location)
    session.commit()

    location = session.scalar(
        select(LocationTable).where(LocationTable.latitude_longitude == point)
    )
    return location
