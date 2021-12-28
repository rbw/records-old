class BootstrappingError(Exception):
    """Application initialization errors"""


class RequestError(Exception):
    detail = None
    orig = None

    def __init__(self, detail, orig=None):
        self.detail = detail
        self.orig = orig


class NoSuchRecord(RequestError):
    """Requested record doesn't exist"""


class PayloadDecodeError(RequestError):
    """Error decoding the request JSON body"""


class PayloadValidationError(RequestError):
    """Payload of a POST request failed validation"""


class NoDatabaseAccess(RequestError):
    """Database access was attempted on a Service without a database attached"""
