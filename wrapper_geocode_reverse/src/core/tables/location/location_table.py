from geoalchemy2 import Geometry, WKBElement
from sqlalchemy.orm import Mapped, mapped_column

from wrapper_geocode_reverse.src.core.tables.default_table import (
    DefaultTable,
)


class LocationTable(DefaultTable):
    __tablename__ = 'location'

    longitude: Mapped[float]
    latitude: Mapped[float]

    latitude_longitude: Mapped[WKBElement] = mapped_column(
        Geometry(
            geometry_type='POINT',
            srid=4326,
            spatial_index=True,
        ),
        doc="""
               Column definition to save location latitude and longitude and
               used in specific functions for distance calculation
            """,
    )

    address: Mapped[str]
    city: Mapped[str]
    state: Mapped[str]
    country: Mapped[str]
    postal_code: Mapped[str]
