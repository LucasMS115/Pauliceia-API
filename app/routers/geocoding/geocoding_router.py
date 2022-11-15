from fastapi import APIRouter

from app.managers.geocoding_manager import *
from app.models.geocoding_models import GeolocationPoint, Street
from app.routers.geocoding.error_responses_examples import *

router = APIRouter(prefix="/geocoding", tags=["geocoding"])


@router.get('/geolocation', response_model=GeolocationPoint, responses={**geolocation_error_responses})
async def geolocation(street: str, number: int, year: int):
    return get_geolocation(street, number, year)


@router.get('/addresses', response_model=list[str], responses={**addresses_error_responses})
async def get_addresses():
    return get_places_list()


@router.get('/streets', response_model=list[Street], responses={**streets_error_responses})
async def list_streets():
    return get_streets_list()
