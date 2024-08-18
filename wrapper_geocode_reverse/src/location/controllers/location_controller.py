from typing import List

from geoalchemy2.functions import ST_DWithin, ST_GeogFromText
from pydantic import PositiveFloat
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..schemas.location_schema import LocationServiceModel
from ..tables.location_table import LocationTable


def insert_locations(locations: List[LocationServiceModel], session: Session):
    locations_insert = [
        LocationTable.from_service(location_db) for location_db in locations
    ]

    session.add_all(locations_insert)
    session.commit()


def get_location_by_latitude_longitude(
    session: Session,
    point: ST_GeogFromText,
    min_confidence: PositiveFloat,
    km_distance,
    number_points: int = 10,
):
    locations = session.scalars(
        select(LocationTable)
        .where(
            ST_DWithin(LocationTable.latitude_longitude, point, km_distance)
        )
        .where(LocationTable.confidence >= min_confidence)
        .limit(number_points)
        .order_by(LocationTable.confidence.desc()),
    ).all()

    return locations
