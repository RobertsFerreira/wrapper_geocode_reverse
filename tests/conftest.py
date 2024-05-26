import os

import pytest
from fastapi.testclient import TestClient
from geoalchemy2 import load_spatialite
from sqlalchemy import create_engine
from sqlalchemy.event import listen
from sqlalchemy.orm import Session

from wrapper_geocode_reverse.app import app
from wrapper_geocode_reverse.src.tables.location_table import table_registry


@pytest.fixture()
def client():
    return TestClient(app)


@pytest.fixture()
def session():
    engine = create_engine('sqlite:///:memory:')

    base_path = "E:\\ProjetosPY\\wrapper_geocode_reverse"
    path = f'{base_path}\\plugins\\spatialite\\mod_spatialite.dll'

    os.environ['SPATIALITE_LIBRARY_PATH'] = path

    listen(engine, 'connect', load_spatialite)
    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    table_registry.metadata.drop_all(engine)
