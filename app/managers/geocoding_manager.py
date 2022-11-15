import pydantic
import json
from fastapi import HTTPException
from httpx import Response
from http import HTTPStatus

from app.models.geocoding_models import GeolocationPoint, Street
from app.services_urls import GEOCODING_URL
from app.utils.request_utils import do_service_request, get_response_json
from app.utils.error_utils import mount_errors_dict


def get_geolocation(street: str, number: int, year: int, path: str = "/geocoding/geolocation"):
    get_geolocation_url: str = f"{GEOCODING_URL}/geolocation/{street},{number},{year}/json"
    response: Response = do_service_request("Geocoding", get_geolocation_url, path)

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


def get_places_list(path: str = "/geocoding/addresses"):
    url: str = f"{GEOCODING_URL}/placeslist"
    response: Response = do_service_request("Geocoding", url, path)
    response_list: list = get_response_json("Geocoding", response, path)

    return response_list


def get_streets_list(path: str = "/geocoding/streets"):
    url: str = f"{GEOCODING_URL}/streets"
    response: Response = do_service_request("Geocoding", url, path)
    response_list: list = get_response_json("Geocoding", response, path)
    parsed_response_list = parse_streets_list(response_list, path)

    return parsed_response_list


def parse_streets_list(response_list: list, path: str):
    try:
        parsed_streets_list: list[Street] = list(map(parse_street_dict, response_list))
    except (pydantic.error_wrappers.ValidationError, KeyError) as error:
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                            detail=mount_errors_dict(HTTPStatus.INTERNAL_SERVER_ERROR,
                                                     str(error),
                                                     "Geocoding service returned an invalid list for streets.",
                                                     path))

    return parsed_streets_list


def parse_street_dict(street: dict):
    # todo: analyse if the streets without name are valid. Decide if they have to be removed.
    # if street['street_name'] is None:
        # do something

    return Street.parse_obj(street)
