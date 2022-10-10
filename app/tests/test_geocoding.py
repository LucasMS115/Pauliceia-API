from fastapi.testclient import TestClient
from http import HTTPStatus
import httpx

from app.main import app
from app.services_urls import GEOCODING_URL

client = TestClient(app)
GEOCODING_PREFIX: str = "/geocoding"
GEOLOCATION_PATH: str = f"{GEOCODING_PREFIX}/geolocation"
ADDRESSES_PATH: str = f"{GEOCODING_PREFIX}/addresses"


def test_get_geolocation_success(respx_mock):
    service_request_url: str = f"{GEOCODING_URL}/geolocation/alameda%20barao%20de%20piracicaba,34,1908/json"

    service_response_mock = [
        {
            "createdAt": "11:16:57 10/10/2022",
            "type": "GET"
        },
        [
            {
                "name": "",
                "geom": "POINT(-46.6497329689309 -23.5333552136211)",
                "confidence": 1,
                "status": 1
            }
        ]
    ]

    params = {"street": "alameda barao de piracicaba",
              "number": "34",
              "year": "1908"}

    respx_mock.get(service_request_url).mock(return_value=httpx.Response(HTTPStatus.OK, json=service_response_mock))
    response = client.get('/geocoding/geolocation', params=params)
    response_body = response.json()

    assert response.status_code == HTTPStatus.OK
    assert response_body['name'] == ""
    assert response_body['geom'] == "POINT(-46.6497329689309 -23.5333552136211)"
    assert response_body['confidence'] == 1
    assert response_body['status'] == 1


def test_get_geolocation_invalid_geo_point(respx_mock):
    service_request_url: str = f"{GEOCODING_URL}/geolocation/alameda%20barao%20de%20piracicaba,34,1908/json"

    service_response_mock = [
        {
            "createdAt": "11:16:57 10/10/2022",
            "type": "GET"
        },
        [
            {
                "name": "",
                "confidence": 1,
                "status": 1
            }
        ]
    ]

    params = {"street": "alameda barao de piracicaba",
              "number": "34",
              "year": "1908"}

    respx_mock.get(service_request_url).mock(return_value=httpx.Response(HTTPStatus.OK, json=service_response_mock))
    response = client.get(GEOLOCATION_PATH, params=params)
    error_detail = response.json()['detail']

    assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
    assert "geom" in error_detail['error']
    assert error_detail['message'] == "Geocoding service returned an invalid geolocation point."
    assert error_detail['path'] == GEOLOCATION_PATH


def test_get_geolocation_not_found(respx_mock):
    service_request_url: str = f"{GEOCODING_URL}/geolocation/alameda%20barao%20da%20pisadinha,34,1908/json"

    service_response_mock = [
        {
            "createdAt": "11:32:45 10/10/2022",
            "type": "GET"
        },
        [
            {
                "name": "Point not found",
                "alertMsg": "Não encontramos pontos nesse logradouro referentes ao ano buscado (alameda barao da "
                            "pisadinha, 34, 1908)",
                "status": 0
            }
        ]
    ]

    params = {"street": "alameda barao da pisadinha",
              "number": "34",
              "year": "1908"}

    respx_mock.get(service_request_url).mock(return_value=httpx.Response(HTTPStatus.OK, json=service_response_mock))
    response = client.get(GEOLOCATION_PATH, params=params)
    error_detail = response.json()['detail']

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert error_detail['error'] == "Point not found"
    assert error_detail['message'] == "Address: alameda barao da pisadinha,34,1908"
    assert error_detail['path'] == GEOLOCATION_PATH


def test_get_geolocation_server_error(respx_mock):
    service_request_url: str = f"{GEOCODING_URL}/geolocation/alameda%20barao%20de%20piracicaba,34,1908/json"
    service_response_mock = {"error": "Service unavailable"}
    params = {"street": "alameda barao de piracicaba",
              "number": "34",
              "year": "1908"}

    respx_mock.get(service_request_url).mock(return_value=httpx.Response(HTTPStatus.OK, json=service_response_mock))
    response = client.get(GEOLOCATION_PATH, params=params)
    error_detail = response.json()['detail']

    assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
    assert error_detail['error'] == "Invalid json"
    assert error_detail['message'] == "Geocoding service couldn't return a valid json."
    assert error_detail['path'] == GEOLOCATION_PATH


def test_get_addresses_success(respx_mock):
    service_request_url: str = f"{GEOCODING_URL}/placeslist"
    service_response_mock = ["alameda barao de piracicaba, 34, 1908", "alameda barao de piracicaba, 59, 1908"]
    respx_mock.get(service_request_url).mock(return_value=httpx.Response(HTTPStatus.OK, json=service_response_mock))
    response = client.get(ADDRESSES_PATH)
    response_body = response.json()

    assert response.status_code == HTTPStatus.OK
    assert len(response.json()) == 2
    assert response_body[0] == "alameda barao de piracicaba, 34, 1908"
    assert response_body[1] == "alameda barao de piracicaba, 59, 1908"
