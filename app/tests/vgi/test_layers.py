from fastapi.testclient import TestClient
import httpx
from http import HTTPStatus

from app.main import app
from app.services_urls import VGI_URL

client = TestClient(app)
LAYERS_PATH: str = "/vgi/layers"


def test_get_all_layers(respx_mock):
    service_request_url: str = f"{VGI_URL}/layer"
    service_response_mock = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Layer",
                "properties": {
                    "name": "Streets Pilot Area",
                    "keyword": [
                        1040
                    ],
                    "layer_id": 2,
                    "reference": None,
                    "created_at": "2019-01-30 18:06:39",
                    "description": "",
                    "f_table_name": "streets_pilot_area",
                    "source_description": ""
                }
            },
            {
                "type": "Layer",
                "properties": {
                    "name": "Places Pilot Area",
                    "keyword": [
                        1040
                    ],
                    "layer_id": 3,
                    "reference": None,
                    "created_at": "2019-01-30 18:06:39",
                    "description": "",
                    "f_table_name": "places_pilot_area2",
                    "source_description": ""
                }
            },
            {
                "type": "Layer",
                "properties": {
                    "name": "Rotas Invisiveis",
                    "keyword": [
                        20,
                        1040
                    ],
                    "layer_id": 37,
                    "reference": [
                        11,
                        12
                    ],
                    "created_at": "2019-05-06 14:29:05",
                    "description": "Caminhos indígenas que originaram ruas de São Paulo",
                    "f_table_name": "rotas_invisiveis",
                    "source_description": "Caminhos indígenas que originaram ruas de São Paulo"
                }
            }
        ]
    }

    respx_mock.get(service_request_url).mock(return_value=httpx.Response(HTTPStatus.OK, json=service_response_mock))
    response = client.get(LAYERS_PATH)
    response_body = response.json()

    assert response.status_code == HTTPStatus.OK
    assert len(response_body) == 3
    assert response_body[2]['name'] == "Rotas Invisiveis"
    assert response_body[2]['layer_id'] == 37
    assert response_body[2]['description'] == "Caminhos indígenas que originaram ruas de São Paulo"
    assert response_body[2]['f_table_name'] == "rotas_invisiveis"
    assert response_body[2]['source_description'] == "Caminhos indígenas que originaram ruas de São Paulo"
    assert len(response_body[2]['keyword']) == 2
    assert len(response_body[2]['reference']) == 2
    assert response_body[2]['created_at'] == "2019-05-06 14:29:05"


def test_get_layer_by_id(respx_mock):
    service_request_url: str = f"{VGI_URL}/layer"
    service_response_mock = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Layer",
                "properties": {
                    "name": "Rotas Invisiveis",
                    "keyword": [
                        20,
                        1040
                    ],
                    "layer_id": 37,
                    "reference": [
                        11,
                        12
                    ],
                    "created_at": "2019-05-06 14:29:05",
                    "description": "Caminhos indígenas que originaram ruas de São Paulo",
                    "f_table_name": "rotas_invisiveis",
                    "source_description": "Caminhos indígenas que originaram ruas de São Paulo"
                }
            },

        ]
    }

    respx_mock.get(url__eq=f"{service_request_url}?layer_id=2").mock(return_value=httpx.Response(HTTPStatus.OK, json=service_response_mock))
    response = client.get(LAYERS_PATH, params={"layer_id": 2})
    response_body = response.json()

    assert response.status_code == HTTPStatus.OK
    assert len(response_body) == 1
    assert response_body[0]['name'] == "Rotas Invisiveis"
    assert response_body[0]['layer_id'] == 37
    assert response_body[0]['description'] == "Caminhos indígenas que originaram ruas de São Paulo"
    assert response_body[0]['f_table_name'] == "rotas_invisiveis"
    assert response_body[0]['source_description'] == "Caminhos indígenas que originaram ruas de São Paulo"
    assert len(response_body[0]['keyword']) == 2
    assert len(response_body[0]['reference']) == 2
    assert response_body[0]['created_at'] == "2019-05-06 14:29:05"


def test_get_layers_server_error(respx_mock):
    service_request_url: str = f"{VGI_URL}/layer"

    respx_mock.get(service_request_url).mock(side_effect=httpx.HTTPError("Internal server error"))
    response = client.get(LAYERS_PATH)
    error_detail = response.json()['detail']

    assert response.status_code == HTTPStatus.SERVICE_UNAVAILABLE
    assert error_detail['error'] == "Internal server error"
    assert error_detail['message'] == "Couldn't get a response from VGI service."
    assert error_detail['path'] == LAYERS_PATH


def test_invalid_list_of_features(respx_mock):
    service_request_url: str = f"{VGI_URL}/layer"
    service_response_mock = {
        "type": "FeatureCollection"
    }

    respx_mock.get(service_request_url).mock(return_value=httpx.Response(HTTPStatus.OK, json=service_response_mock))
    response = client.get(LAYERS_PATH)
    error_detail = response.json()['detail']

    assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
    assert error_detail['error'] == "Invalid json"
    assert error_detail['message'] == "VGI service couldn't return a valid list of features."
    assert error_detail['path'] == LAYERS_PATH


def test_invalid_list_of_layers(respx_mock):
    service_request_url: str = f"{VGI_URL}/layer"
    service_response_mock = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Layer",
                "properties": {
                    "name": "Rotas Invisiveis",
                    "keyword": [
                        20,
                        1040
                    ],
                    "reference": [
                        11,
                        12
                    ],
                    "created_at": "2019-05-06 14:29:05",
                    "description": "Caminhos indígenas que originaram ruas de São Paulo",
                    "f_table_name": "rotas_invisiveis",
                    "source_description": "Caminhos indígenas que originaram ruas de São Paulo"
                }
            }
        ]
    }

    respx_mock.get(service_request_url).mock(return_value=httpx.Response(HTTPStatus.OK, json=service_response_mock))
    response = client.get(LAYERS_PATH)
    error_detail = response.json()['detail']

    assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
    assert "layer_id" in error_detail['error']
    assert error_detail['message'] == "VGI service returned an invalid list of layers."
    assert error_detail['path'] == LAYERS_PATH

