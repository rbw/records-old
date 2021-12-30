import logging
from abc import ABC, ABCMeta


class ServiceMeta(ABCMeta):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(ServiceMeta, cls).__call__(*args, **kwargs)

        return cls._instances[cls]


class BaseService(ABC):
    def __init__(self, app):
        self.log = logging.getLogger(__name__)
        self.app = app
