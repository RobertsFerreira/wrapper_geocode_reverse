from pydantic import BaseModel, Field


class LocationServiceModel(BaseModel):
    address: str
    city: str = Field(alias='locality')
    state: str
    country: str
    postal_code: str
    latitude: float
    longitude: float
