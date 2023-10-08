from abc import ABC, abstractmethod
from requests import Session


class BaseSession(ABC):
    @abstractmethod
    def get(self, *args, **kwargs):
        pass


class RequestSession(Session, BaseSession):
    pass
