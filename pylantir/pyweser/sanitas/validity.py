# -*- coding: utf-8 -*-
"""
Created on Tue Sep 27 13:52:11 2022

@author: gi11883
"""
from abc import ABCMeta
from enum import EnumMeta, Flag
from typing import Any


class ABCEnumMeta(ABCMeta, EnumMeta):
    """abstract meta enum class"""

    # https://stackoverflow.com/questions/56131308/create-an-abstract-enum-class
    def __new__(cls, *args, **kw):
        abstract_enum_cls = super().__new__(cls, *args, **kw)
        # Only check abstractions if members were defined.
        if abstract_enum_cls._member_map_:
            try:  # Handle existence of undefined abstract methods.
                absmethods = list(abstract_enum_cls.__abstractmethods__)
                if absmethods:
                    missing = ", ".join(f"{method!r}" for method in absmethods)
                    plural = "s" if len(absmethods) > 1 else ""
                    raise TypeError(
                        f"cannot instantiate abstract class {abstract_enum_cls.__name__!r}"
                        f" with abstract method{plural} {missing}"
                    )
            except AttributeError:
                pass
        return abstract_enum_cls


class EnumType(Flag, metaclass=ABCEnumMeta):
    """enum abstract class for types validation"""

    def __str__(self):
        """return the type in form of a string"""

    @property
    def type(self):
        """return a tuple with the data type"""

    def cast(self, value: Any) -> Any:
        """cast value to the self.type"""


class TypeValidator:
    """validate the type of the provided values"""

    def __init__(self, source: Any, types: list[EnumType]) -> None:
        self.source = source
        self.types = types

    def validate(self):
        """validate the type and store the provided data"""
        source = self.source
        slots = source.__slots__
        types = self.types
        for type_, name in zip(types, slots):
            value = source.__getattribute__(name)
            try:
                source.__setattr__(name, type_.cast(value))
            except TypeError as exc:
                raise TypeError(
                    f"tha argument {name} must be a {str(type_)}"
                ) from exc
