#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 20 15:58:23 2022

@author: gi11883
"""
# import pdb
from dataclasses import dataclass
from enum import auto
from typing import Union
from pylantir.pyweser.sanitas import EnumType, TypeValidator


@dataclass(slots=True)
class Material:
    """.. _Material:

    Simple material dataclass.

    :param name: name of the material
    :type name: str
    :param specification: specification of the material (e.g. AIMS or ABS)
    :type specification: str
    """

    name: str
    specification: str


class PropertyType(EnumType):
    """.. _PropertyType:

    Material properties *enum* class: PropertyType.STR for string,
    PropertyType.NUM for numbers (integers are casted as float).
    """

    STR = auto()  # string
    NUM = auto()  # float, integers are converted to float

    def __str__(self):
        """Return the type as 'string' or 'number'"""
        if self is PropertyType.STR:
            return "string"
        return "number"

    @property
    def type(self) -> tuple:
        """
        Return a tuple with the data types: (str,) for STR and (float, int)
        for NUM.

        :type: tuple of types
        """
        if self is PropertyType.STR:
            return (str,)
        return (float, int)

    def cast(self, value: Union[str, int, float]) -> Union[str, float]:
        """:method:
        cast the provided value to a string or a float accordingly to the type.
        This method is used by the module sanitas to validate the type.

        :param value: value to be casted
        :type value: str, int, float

        :return: value casted accordingly to the PropertyType (STR or NUM).
        :rtype: str (STR) or float (NUM)
        """
        if isinstance(value, self.type):
            return self.type[0](value)
        raise TypeError(f"the argument must be a {str(self)}")


@dataclass(slots=True, kw_only=True)
class OrthoMaterial(Material):
    """.. _OrthoMaterial:

    Class to represent an orthotropic material. The required arguments are: E1, 
    E2, G12, nu12. The optional arguments, if not provided, are set to 0.0
    by default.

    :param E1: Young's modulus along direction 1 (0 degrees)
    :type E1: int, float
    :param E2: Young's modulus along direction 2 (90 degrees)
    :type E2: int, float
    :param E3: Young's modulus along direction 3 (through-the-thicknees)
    :type E3: int, float
    :param G12: shear modulus in the plane 1-2
    :type G12: int, float
    :param G13: shear modulus in the plane 1-3
    :type G13: int, float
    :param G23: shear modulus in the plane 2-3
    :type G23: int, float
    :param nu12: Poisson's ratio in the plane 1-2
    :type nu12: int, float
    :param nu13: Poisson's ratio in the plane 1-3
    :type nu13: int, float
    :param nu23: Poisson's ratio in the plane 2-3
    :type nu23: int, float
    """

    E1: float
    E2: float
    E3: float = 0.0
    G12: float
    G13: float = 0.0
    G23: float = 0.0
    nu12: float
    nu13: float = 0.0
    nu23: float = 0.0

    def __post_init__(self):
        # validate the properties
        _num_ = PropertyType.NUM
        _str_ = PropertyType.STR
        types = [_str_] * 2 + [_num_] * 9
        TypeValidator(self, types).validate()


@dataclass(slots=True, kw_only=True)
class IsoMaterial(Material):
    """.. _IsoMaterial:

    Class to represent an isotropic material

    :param E: Young's modulus along direction 1 (0 degrees)
    :type E: int, float
    :param G: shear modulus in the plane
    :type G: int, float
    :param nu: Poisson's ratio'
    :type nu: float
    """

    E: float
    G: float = 0.0
    nu: float = 0.0

    def __post_init__(self):
        # validate the type of the properties
        _num_ = PropertyType.NUM
        _str_ = PropertyType.STR
        types = [_str_] * 2 + [_num_] * 3
        TypeValidator(self, types).validate()
        # derive G or nu if one of the two is missing
        E = self.E
        G = self.G
        nu = self.nu
        if G != 0.0 and nu != 0.0:
            pass
        elif G == 0.0 and nu != 0.0:
            self.G = E / 2.0 / (1.0 + nu)
        elif G != 0.0 and nu == 0.0:
            self.nu = E / G / 2.0 - 1.0
        else:
            raise TypeError(
                "IsoMaterial.__init__() missing 1 required keyword-only argument: either 'G' or 'nu' must be provided with 'E'"
            )
