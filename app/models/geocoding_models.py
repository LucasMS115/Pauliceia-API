from typing import Optional
from pydantic import BaseModel


class GeolocationPoint(BaseModel):
    name: str
    geom: str
    confidence: int
    status: int


class Street(BaseModel):
    id: int
    street_name: Optional[str] = None   # todo: analyse if the streets without name are valid.
    street_geom: str
    street_firstyear: int
    street_lastyear: int
