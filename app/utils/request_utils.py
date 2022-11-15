import json
import httpx
from httpx import Response
from http import HTTPStatus
from fastapi import HTTPException

from app.utils.error_utils import mount_errors_dict


def do_service_request(service_name: str, request_url: str, path: str):
    try:
        return httpx.get(request_url)
    except httpx.HTTPError as error:
        raise HTTPException(status_code=HTTPStatus.SERVICE_UNAVAILABLE,
                            detail=mount_errors_dict(HTTPStatus.INTERNAL_SERVER_ERROR,
                                                     str(error),
                                                     f"Couldn't get a response from {service_name} service.",
                                                     path))


def get_response_json(service_name: str, response: Response, path: str):
    try:
        response = response.json()
    except json.JSONDecodeError as error:
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                            detail=mount_errors_dict(HTTPStatus.INTERNAL_SERVER_ERROR,
                                                     str(error),
                                                     f"{service_name} service couldn't return a valid json.",
                                                     path))

    return response
