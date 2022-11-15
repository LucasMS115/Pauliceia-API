import json
import pydantic
from fastapi import HTTPException
from http import HTTPStatus
from httpx import Response

from app.models.vgi_models import Layer
from app.services_urls import VGI_URL
from app.utils.error_utils import mount_errors_dict
from app.utils.request_utils import do_service_request


def get_layers(layer_id: int = None, path: str = "/vgi/layers"):
    params = {"layer_id": layer_id} if layer_id is not None else None
    response: Response = do_service_request("VGI", f"{VGI_URL}/layer", path, params)
    layers = parse_layers_list(get_features_at_response(response, path), path)

    return layers


def get_features_at_response(response: Response, path: str):
    try:
        response_features = response.json()["features"]
    except (json.JSONDecodeError, KeyError):
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                            detail=mount_errors_dict(HTTPStatus.INTERNAL_SERVER_ERROR,
                                                     "Invalid json",
                                                     "VGI service couldn't return a valid list of features.",
                                                     path))

    return response_features


def parse_layers_list(response_features: list, path: str):
    try:
        parsed_layers_list: list[Layer] = list(map(parse_feature_layer_dict, response_features))
    except (pydantic.error_wrappers.ValidationError, KeyError) as error:
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                            detail=mount_errors_dict(HTTPStatus.INTERNAL_SERVER_ERROR,
                                                     str(error),
                                                     "VGI service returned an invalid list of layers.",
                                                     path))

    return parsed_layers_list


def parse_feature_layer_dict(feature_layer: dict):
    return Layer.parse_obj(feature_layer["properties"])

