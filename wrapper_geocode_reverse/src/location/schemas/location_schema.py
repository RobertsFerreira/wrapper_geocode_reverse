from pydantic import BaseModel, Field
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
