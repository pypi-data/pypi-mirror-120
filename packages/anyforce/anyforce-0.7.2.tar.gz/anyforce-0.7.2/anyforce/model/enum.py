from __future__ import annotations

from enum import Enum as EnumBase
from enum import IntEnum as IntEnumBase
from typing import Any, Optional, Type


class EnumMissingError(Exception):
    def __init__(self, enum_type: Type[EnumBase], value: Any, *args: Any) -> None:
        super().__init__(*args)
        self.enum_type = enum_type
        self.value = value


class Enum(EnumBase):
    def __new__(cls, value: Any, doc: Optional[str] = None):
        self = object.__new__(cls)
        self._value_ = value
        if doc is not None:
            self.__doc__ = doc
        return self

    @classmethod
    def _missing_(cls, value: Any):
        raise EnumMissingError(cls, value, f"枚举值 {value} 不存在")


class IntEnum(IntEnumBase):
    def __new__(cls, value: int, doc: Optional[str] = None):
        self = int.__new__(cls, value)
        self._value_ = value
        if doc is not None:
            self.__doc__ = doc
        return self

    @classmethod
    def _missing_(cls, value: Any):
        raise EnumMissingError(cls, value, f"枚举值 {value} 不存在")
