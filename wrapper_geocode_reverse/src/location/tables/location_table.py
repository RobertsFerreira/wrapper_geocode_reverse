from datetime import datetime

from geoalchemy2 import Geometry, WKBElement
from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, registry

from wrapper_geocode_reverse.src.location.schemas.location_schema import (
    LocationServiceModel,
)

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

    @staticmethod
    def from_service(location: LocationServiceModel):
        point = f'POINT({location.latitude} {location.longitude})'
        return LocationTable(
            latitude=location.latitude,
            longitude=location.longitude,
            confidence=location.confidence,
            address=location.address,
            city=location.city,
            state=location.state,
            country=location.country,
            postal_code=location.postal_code,
            abbreviation_state=location.abbreviation_state,
            abbreviation_country=location.abbreviation_country,
            house_number=location.house_number,
            distance=location.distance,
            latitude_longitude=point,  # type: ignore
        )
