from typing import List

from geoalchemy2.functions import ST_DWithin, ST_GeogFromText
from pydantic import PositiveFloat
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from wrapper_geocode_reverse.src.core.logger.logger import logger

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
    statement_totally_locations = (
        select(func.count(LocationTable.id).label('num_locations'))
        .where(
            ST_DWithin(
                LocationTable.latitude_longitude,
                point,
                km_distance,
            )
        )
        .group_by(LocationTable.id)
    )

    totally_locations = session.execute(statement_totally_locations).all()

    match(totally_locations):
        case []:
            return None
        case ('num_locations', total) if total < 0:
            return None
        case _:
            logger.error(
                'Invalid result for number of totally locations found: %s',
                  totally_locations
            )

    statement = (
        select(LocationTable)
        .where(
            ST_DWithin(
                LocationTable.latitude_longitude,
                point,
                km_distance,
            )
        )
        .where(LocationTable.confidence >= min_confidence)
        .limit(number_points)
        .order_by(LocationTable.confidence.desc())
    )

    sql = statement.compile(compile_kwargs={'literal_binds': True})

    logger.debug('sql query: %s', sql)

    locations = session.scalars(statement).all()

    if len(locations) < number_points:
        return []

    return locations
