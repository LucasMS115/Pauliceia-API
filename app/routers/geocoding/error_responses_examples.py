from http import HTTPStatus

from app.utils.error_utils import mount_example_object


SERVICE_NAME = "Geocoding"

geolocation_error_responses = {
    int(HTTPStatus.INTERNAL_SERVER_ERROR): mount_example_object(
            HTTPStatus.INTERNAL_SERVER_ERROR,
            "<error-str>",
            "Geocoding service returned an invalid geolocation point.",
            "/geocoding/geolocation"),

    int(HTTPStatus.SERVICE_UNAVAILABLE): mount_example_object(
        HTTPStatus.SERVICE_UNAVAILABLE,
        "<error-str>",
        f"Couldn't get a response from {SERVICE_NAME} service.",
        "/geocoding/geolocation"),

    int(HTTPStatus.NOT_FOUND): mount_example_object(
            HTTPStatus.NOT_FOUND,
            "Point not found",
            "Address: <address>",
            "/geocoding/geolocation"),
}


addresses_error_responses = {
    int(HTTPStatus.INTERNAL_SERVER_ERROR): mount_example_object(
        HTTPStatus.INTERNAL_SERVER_ERROR,
        "<error-str>",
        f"{SERVICE_NAME} service couldn't return a valid json.",
        "/geocoding/addresses"),

    int(HTTPStatus.SERVICE_UNAVAILABLE): mount_example_object(
        HTTPStatus.SERVICE_UNAVAILABLE,
        "<error-str>",
        f"Couldn't get a response from {SERVICE_NAME} service.",
        "/geocoding/addresses"),
}

streets_error_responses = {
    int(HTTPStatus.INTERNAL_SERVER_ERROR): mount_example_object(
        HTTPStatus.INTERNAL_SERVER_ERROR,
        "<error-str>",
        "Geocoding service returned an invalid list for streets.",
        "/geocoding/streets"),

    int(HTTPStatus.SERVICE_UNAVAILABLE): mount_example_object(
        HTTPStatus.SERVICE_UNAVAILABLE,
        "<error-str>",
        f"Couldn't get a response from {SERVICE_NAME} service.",
        "/geocoding/streets"),
}