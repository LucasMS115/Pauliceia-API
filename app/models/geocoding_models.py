from pydantic import BaseModel


class GeolocationPoint(BaseModel):
    name: str
    geom: str
    confidence: int
    status: int
