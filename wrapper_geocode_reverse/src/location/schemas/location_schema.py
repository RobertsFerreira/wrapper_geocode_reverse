from pydantic import BaseModel


class LocationServiceModel(BaseModel):
    address: str
    city: str
    state: str
    country: str
    postal_code: str
    latitude: float
    longitude: float
