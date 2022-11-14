"""Defines interface of generic map type String StrMap."""

import abc
from typing import Any, Optional, Tuple, List


class StrMapPosition(abc.ABC):
    pass


class StrMap(abc.ABC):
    """Generic StrMap container interface using string keys."""

    @abc.abstractmethod
    def __getitem__(self, key: str) -> Any:
        raise NotImplementedError

    @abc.abstractmethod
    def __setitem__(self, key: str, value: Any) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def __contains__(self, key: str) -> bool:
        raise NotImplementedError

    @abc.abstractmethod
    def __len__(self) -> int:
        raise NotImplementedError

    @abc.abstractmethod
    def __iter__(self):
        raise NotImplementedError

    @abc.abstractmethod
    def __str__(self) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    def __delitem__(self, key: str) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def at_position(self, position: StrMapPosition) -> Tuple[str, Any]:
        raise NotImplementedError

    @abc.abstractmethod
    def find_position(self, key: str) -> Optional[StrMapPosition]:
        raise NotImplementedError

    @abc.abstractmethod
    def items(self) -> List[Tuple[str, Any]]:
        raise NotImplementedError
