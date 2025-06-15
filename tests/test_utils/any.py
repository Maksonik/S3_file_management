from collections.abc import Iterable
from datetime import datetime
from typing import Union
from unittest import mock
from uuid import UUID


class AnyType:
    """Enable to check a type of a value without equality comparison."""

    def __init__(self, types: Union[type, Iterable[type]]):
        self.types = tuple(types) if not isinstance(types, type) else (types,)

    def __eq__(self, other: object):
        return isinstance(other, self.types)

    def __repr__(self):
        return f"instance of {[x.__qualname__ for x in self.types]}"


ANY = mock.ANY
ANY_INT = AnyType(int)
ANY_STR = AnyType(str)
ANY_DICT = AnyType(dict)
ANY_LIST = AnyType(list)
ANY_BOOL = AnyType(bool)
ANY_DATETIME = AnyType(datetime)
ANY_UUID = AnyType(UUID)
