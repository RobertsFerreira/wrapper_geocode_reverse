from sqlalchemy import select

from wrapper_geocode_reverse.src.core.tables.location.location_table import (
    LocationTable,
)


def test_create_location(session):
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

    assert location.latitude == latitude
    assert location.longitude == longitude
