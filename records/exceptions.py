import json


class BootstrappingError(Exception):
    """Application initialization errors"""


class RequestError(Exception):
    detail = None

    def __init__(self, detail):
        self.detail = detail


class MissingRouter(BootstrappingError):
    """Raised if a route module is missing the `router` attribute"""


class NoSuchRecord(RequestError):
    """Raised if the requested record doesn't exist"""


class DatabaseInsertError(RequestError):
    """Raised if there was an error creating a new record in the database"""


class PayloadDecodeError(RequestError):
    """Raised if there was an error decoding the request JSON body"""


class PayloadValidationError(RequestError):
    """Raised if the payload of a POST request failed validation"""
