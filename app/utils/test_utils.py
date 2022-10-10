from datetime import datetime


def mount_errors_dict(status: int, error: str, message: str, path: str):
    return {
               "timestamp": datetime.now().ctime(),
               "status": status,
               "error": error,
               "message": message,
               "path": path,
           }
