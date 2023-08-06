import abc
from typing import Any

from .model import AggregateRoot


class AggregateRootNotFoundException(RuntimeError):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class Finder(metaclass=abc.ABCMeta):
    AggregateRootNotFoundException = AggregateRootNotFoundException

    @abc.abstractmethod
    def find(self, id: Any) -> AggregateRoot:
        raise NotImplementedError
