from fastapi import APIRouter

from app.managers.geocoding_manager import *
from app.models.geocoding_models import GeolocationPoint, Street

router = APIRouter(prefix="/geocoding", tags=["geocoding"])


@router.get('/geolocation', response_model=GeolocationPoint)
async def geolocation(street: str, number: int, year: int):

    return get_geolocation(street, number, year)


@router.get('/addresses', response_model=list[str])
async def get_addresses():

    return get_places_list()


@router.get('/streets', response_model=list[Street])
async def list_streets():

    return get_streets_list()
