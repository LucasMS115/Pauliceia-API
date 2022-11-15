from datetime import datetime
from http import HTTPStatus


def mount_errors_dict(status: int, error: str, message: str, path: str):
    return {
               "timestamp": datetime.now().ctime(),
               "status": status,
               "error": error,
               "message": message,
               "path": path,
           }


def mount_example_object(status: int,  error: str, message: str, path: str):
    return{
        "description": HTTPStatus(status).name,
        "content": {
            "application/json": {
                "examples": {
                    "example": {
                        "value": mount_errors_dict(status,
                                                   error,
                                                   message,
                                                   path)
                    },
                }
            }
        }
    }
