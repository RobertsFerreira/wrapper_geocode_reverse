import pytest
from fastapi.testclient import TestClient
from geoalchemy2.functions import ST_DWithin, ST_GeogFromText
from pydantic_extra_types.coordinate import Coordinate, Latitude, Longitude
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from wrapper_geocode_reverse.app import app
from wrapper_geocode_reverse.src.core import Settings, get_session
from wrapper_geocode_reverse.src.location import (
    LocationTable,
)


@pytest.fixture()
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client
    app.dependency_overrides.clear()


@pytest.fixture()
def settings():
    return Settings()  # type: ignore


@pytest.fixture()
def coordinate():
    return Coordinate(
        latitude=Latitude(-21.174267), longitude=Longitude(-43.024593)
    )


@pytest.fixture()
def params_test_location(settings: Settings, coordinate: Coordinate):
    return {
        'api_key': settings.OPEN_ROUTER_TOKEN,
        'point.lon': coordinate.longitude,
        'point.lat': coordinate.latitude,
        'size': 1,
    }


@pytest.fixture()
def session(settings: Settings):
    # engine = create_engine(
    #     'sqlite:///:memory:',
    #     connect_args={'check_same_thread': False},
    #     poolclass=StaticPool,
    # )

    # base_path = 'E:\\ProjetosPY\\wrapper_geocode_reverse'
    # path = f'{base_path}\\plugins\\spatialite\\mod_spatialite.dll'

    # os.environ['SPATIALITE_LIBRARY_PATH'] = path

    # listen(engine, 'connect', load_spatialite)
    engine = create_engine(settings.DATABASE_URL)
    # table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session
        session.rollback()

    # table_registry.metadata.drop_all(engine)


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
        abbreviation_state='abbreviation_state',
        abbreviation_country='abbreviation_country',
        confidence=0.0,
        house_number='house_number',
        distance=0.0,
    )

    session.add(new_location)
    session.commit()

    point_sql = ST_GeogFromText(f'POINT({latitude} {longitude})', srid=4326)

    location = session.scalar(
        select(LocationTable).where(
            ST_DWithin(LocationTable.latitude_longitude, point_sql, 1000)
        )
    )
    return location
