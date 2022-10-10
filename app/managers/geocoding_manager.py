from http import HTTPStatus

import pydantic
from fastapi import HTTPException
import json
import httpx
from httpx import Response

from app.models.geocoding_models import GeolocationPoint
from app.services_urls import GEOCODING_URL
from app.utils.test_utils import mount_errors_dict


def get_geolocation(street: str, number: int, year: int, path: str = "/geocoding/geolocation"):
    get_geolocation_url: str = f"{GEOCODING_URL}/geolocation/{street},{number},{year}/json"
    response: Response = httpx.get(get_geolocation_url)

    response_point = get_geolocation_response_point(response, path)
    check_point_not_found(response_point, f"{street},{number},{year}", path)
    geo_point: GeolocationPoint = get_parsed_geo_point(response_point, path)

    return geo_point


def get_geolocation_response_point(response: Response, path: str):
    try:
        response = response.json()[1][0]
    except (json.JSONDecodeError, KeyError):
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                            detail=mount_errors_dict(HTTPStatus.INTERNAL_SERVER_ERROR,
                                                     "Invalid json",
                                                     "Geocoding service couldn't return a valid json.",
                                                     path))

    return response


def check_point_not_found(response_point: dict, address: str, path: str):
    if response_point['name'] == 'Point not found':
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail=mount_errors_dict(HTTPStatus.NOT_FOUND,
                                                     "Point not found",
                                                     f"Address: {address}",
                                                     path))


def get_parsed_geo_point(response_point: dict, path: str):
    try:
        geo_point: GeolocationPoint = GeolocationPoint.parse_obj(response_point)
    except pydantic.error_wrappers.ValidationError as error:
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                            detail=mount_errors_dict(HTTPStatus.INTERNAL_SERVER_ERROR,
                                                     str(error),
                                                     "Geocoding service returned an invalid geolocation point.",
                                                     path))

    return geo_point


def get_places_list():
    url: str = f"{GEOCODING_URL}/placeslist"
    response: Response = httpx.get(url)

    return response.json()


def get_streets_list():
    url: str = f"{GEOCODING_URL}/streets"
    response: Response = httpx.get(url)

    return response.json()
