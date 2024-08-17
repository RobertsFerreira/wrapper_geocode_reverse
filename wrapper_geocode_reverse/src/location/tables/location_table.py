from datetime import datetime

from geoalchemy2 import Geometry, WKBElement
from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, registry

table_registry = registry()


@table_registry.mapped_as_dataclass
class LocationTable:
    __tablename__ = 'location'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    created_at: Mapped[datetime] = mapped_column(
        init=False,
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        init=False,
        server_default=func.now(),
        onupdate=func.now(),
    )
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
    house_number: Mapped[str]
    city: Mapped[str]
    state: Mapped[str]
    abbreviation_state: Mapped[str]
    country: Mapped[str]
    abbreviation_country: Mapped[str]
    postal_code: Mapped[str]
    distance: Mapped[float]
    confidence: Mapped[float]
