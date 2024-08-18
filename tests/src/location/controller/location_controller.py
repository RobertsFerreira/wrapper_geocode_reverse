import pytest
from geoalchemy2.functions import ST_DWithin, ST_GeogFromText
from sqlalchemy import select
from sqlalchemy.orm import Session

from wrapper_geocode_reverse.src.location import insert_locations
from wrapper_geocode_reverse.src.location.tables.location_table import (
    LocationTable,
)


def test_insert_locations(location_table_model):
    session = Session()

    insert_locations(
        locations=[location_table_model],
        session=session,
    )

    latitude, longitude = 1, 1
    point_sql = ST_GeogFromText(f'POINT({latitude} {longitude})', srid=4326)

    location = session.scalar(
        select(LocationTable).where(
            ST_DWithin(LocationTable.latitude_longitude, point_sql, 1000)
        )
    )

    if location is None:
        pytest.fail('Location not found in the database')

    assert location.latitude == latitude
    assert location.longitude == longitude
