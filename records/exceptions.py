import json


class BootstrappingError(Exception):
    """Application initialization errors"""


class RequestError(Exception):
    detail = None

    def __init__(self, detail):
        self.detail = detail


class NoSuchRecord(RequestError):
    """Requested record doesn't exist"""


class DatabaseInsertError(RequestError):
    """Error creating a new record in the database"""


class PayloadDecodeError(RequestError):
    """Error decoding the request JSON body"""


class PayloadValidationError(RequestError):
    """Payload of a POST request failed validation"""


class NoDatabaseAccess(RequestError):
    """Database access was attempted on a Service without a database attached"""
