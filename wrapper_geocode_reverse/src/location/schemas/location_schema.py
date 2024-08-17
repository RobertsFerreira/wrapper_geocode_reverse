from pydantic import BaseModel, ConfigDict, Field
from pydantic_extra_types.coordinate import Latitude, Longitude


class LocationServiceModel(BaseModel):
    address: str = Field(alias='name')
    house_number: str = Field(alias='housenumber', default='')
    city: str = Field(alias='locality')
    state: str = Field(alias='region')
    abbreviation_state: str = Field(alias='region_a')
    country: str
    abbreviation_country: str = Field(alias='country_a')
    postal_code: str = Field(alias='postalcode', default='')
    distance: float
    confidence: float
    latitude: Latitude = Field(default=0)
    longitude: Longitude = Field(default=0)


class Location(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    address: str
    house_number: str
    city: str
    state: str
    abbreviation_state: str
    country: str
    abbreviation_country: str
    postal_code: str
    distance: float
    confidence: float
    latitude: Latitude
    longitude: Longitude
