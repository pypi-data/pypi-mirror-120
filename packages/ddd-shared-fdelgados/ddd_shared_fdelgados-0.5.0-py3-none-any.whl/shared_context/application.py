from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional
import abc


@dataclass(frozen=True)
class Command(metaclass=abc.ABCMeta):
    pass


class CommandHandler(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def handle(self, command: Command) -> Optional[Response]:
        raise NotImplementedError


@dataclass(frozen=True)
class Query(metaclass=abc.ABCMeta):
    pass


class QueryHandler(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def handle(self, query: Query) -> Response:
        raise NotImplementedError


class Response(metaclass=abc.ABCMeta):
    def to_dict(self) -> Dict:
        return self.__dict__
