from http import HTTPStatus

from app.utils.error_utils import mount_example_object


SERVICE_NAME = "VGI"

get_layers_error_responses = {
    int(HTTPStatus.INTERNAL_SERVER_ERROR): mount_example_object(
            HTTPStatus.INTERNAL_SERVER_ERROR,
            "<error-str>",
            "VGI service couldn't return a valid list of features.",
            "/vgi/layers"),

    int(HTTPStatus.SERVICE_UNAVAILABLE): mount_example_object(
        HTTPStatus.SERVICE_UNAVAILABLE,
        "<error-str>",
        f"Couldn't get a response from {SERVICE_NAME} service.",
        "/vgi/layers")
}

