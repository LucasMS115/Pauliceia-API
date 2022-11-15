from fastapi.testclient import TestClient
import httpx
from http import HTTPStatus

from app.main import app
from app.services_urls import GEOCODING_URL

client = TestClient(app)
GEOCODING_PREFIX: str = "/geocoding"
GEOLOCATION_PATH: str = f"{GEOCODING_PREFIX}/geolocation"
ADDRESSES_PATH: str = f"{GEOCODING_PREFIX}/addresses"
STREETS_PATH: str = f"{GEOCODING_PREFIX}/streets"


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


def test_get_geolocation_server_error(respx_mock):
    service_request_url: str = f"{GEOCODING_URL}/geolocation/alameda%20barao%20de%20piracicaba,34,1908/json"
    params = {"street": "alameda barao de piracicaba",
              "number": "34",
              "year": "1908"}

    respx_mock.get(service_request_url).mock(side_effect=httpx.HTTPError("Internal server error"))
    response = client.get(GEOLOCATION_PATH, params=params)
    error_detail = response.json()['detail']

    assert response.status_code == HTTPStatus.SERVICE_UNAVAILABLE
    assert error_detail['error'] == "Internal server error"
    assert error_detail['message'] == "Couldn't get a response from Geocoding service."
    assert error_detail['path'] == GEOLOCATION_PATH


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


def test_get_geolocation_invalid_response(respx_mock):
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
    assert len(response_body) == 2
    assert response_body[0] == "alameda barao de piracicaba, 34, 1908"
    assert response_body[1] == "alameda barao de piracicaba, 59, 1908"


def test_get_addresses_server_error(respx_mock):
    service_request_url: str = f"{GEOCODING_URL}/placeslist"

    respx_mock.get(service_request_url).mock(side_effect=httpx.HTTPError("Internal server error"))
    response = client.get(ADDRESSES_PATH)
    error_detail = response.json()['detail']

    assert response.status_code == HTTPStatus.SERVICE_UNAVAILABLE
    assert error_detail['error'] == "Internal server error"
    assert error_detail['message'] == "Couldn't get a response from Geocoding service."
    assert error_detail['path'] == ADDRESSES_PATH


def test_get_addresses_invalid_response(respx_mock):
    service_request_url: str = f"{GEOCODING_URL}/placeslist"
    service_response_mock = None

    respx_mock.get(service_request_url).mock(return_value=httpx.Response(HTTPStatus.OK, json=service_response_mock))
    response = client.get(ADDRESSES_PATH)
    error_detail = response.json()['detail']

    assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
    assert error_detail['error'] == "Expecting value: line 1 column 1 (char 0)"
    assert error_detail['message'] == "Geocoding service couldn't return a valid json."
    assert error_detail['path'] == ADDRESSES_PATH


def test_get_streets_success(respx_mock):
    service_request_url: str = f"{GEOCODING_URL}/streets"
    service_response_mock = [
        {
            "id": 146,
            "street_name": "rua doutor almirante lima",
            "street_geom": "MULTILINESTRING((-46.6166040525103 -23.5429721951838,-46.6155725826144 -23.5443667424054,-46.6146490057218 -23.5455807664603,-46.6108867895023 -23.5506516814547,-46.6096410464028 -23.5523598904046,-46.6097361952445 -23.5545989544175))",
            "street_firstyear": 1930,
            "street_lastyear": 1940
        },
        {
            "id": 147,
            "street_name": "rua paulo affonso",
            "street_geom": "MULTILINESTRING((-46.615445146038 -23.5445372347025,-46.6136253300938 -23.5433595337307))",
            "street_firstyear": 1930,
            "street_lastyear": 1940
        },
    ]
    respx_mock.get(service_request_url).mock(return_value=httpx.Response(HTTPStatus.OK, json=service_response_mock))
    response = client.get(STREETS_PATH)
    response_body = response.json()

    assert response.status_code == HTTPStatus.OK
    assert len(response_body) == 2
    assert response_body[0]['id'] == service_response_mock[0]['id']
    assert len(response_body[0]) == 5
    assert response_body[1]['id'] == service_response_mock[1]['id']
    assert len(response_body[1]) == 5


def test_get_streets_server_error(respx_mock):
    service_request_url: str = f"{GEOCODING_URL}/streets"

    respx_mock.get(service_request_url).mock(side_effect=httpx.HTTPError("Internal server error"))
    response = client.get(STREETS_PATH)
    error_detail = response.json()['detail']

    assert response.status_code == HTTPStatus.SERVICE_UNAVAILABLE
    assert error_detail['error'] == "Internal server error"
    assert error_detail['message'] == "Couldn't get a response from Geocoding service."
    assert error_detail['path'] == STREETS_PATH


def test_get_streets_invalid_response(respx_mock):
    service_request_url: str = f"{GEOCODING_URL}/streets"
    service_response_mock = None

    respx_mock.get(service_request_url).mock(return_value=httpx.Response(HTTPStatus.OK, json=service_response_mock))
    response = client.get(STREETS_PATH)
    error_detail = response.json()['detail']

    assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
    assert error_detail['error'] == "Expecting value: line 1 column 1 (char 0)"
    assert error_detail['message'] == "Geocoding service couldn't return a valid json."
    assert error_detail['path'] == STREETS_PATH


def test_get_geolocation_invalid_street(respx_mock):
    service_request_url: str = f"{GEOCODING_URL}/streets"
    service_response_mock = [
        {
            "id": 146,
            "street_name": "rua doutor almirante lima",
            "street_geom": "MULTILINESTRING((-46.6166040525103 -23.5429721951838,-46.6155725826144 -23.5443667424054,-46.6146490057218 -23.5455807664603,-46.6108867895023 -23.5506516814547,-46.6096410464028 -23.5523598904046,-46.6097361952445 -23.5545989544175))",
            "street_firstyear": 1930,
            "street_lastyear": 1940
        },
        {
            "id": 147,
            "street_name": "rua paulo affonso",
            "street_firstyear": 1930,
            "street_lastyear": 1940
        },
    ]

    respx_mock.get(service_request_url).mock(return_value=httpx.Response(HTTPStatus.OK, json=service_response_mock))
    response = client.get(STREETS_PATH)
    error_detail = response.json()['detail']

    assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
    assert "street_geom" in error_detail['error']
    assert error_detail['message'] == "Geocoding service returned an invalid list for streets."
    assert error_detail['path'] == STREETS_PATH
