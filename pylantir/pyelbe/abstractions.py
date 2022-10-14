"""Abstraction Classes"""
from dataclasses import dataclass, field
from collections import namedtuple


#TODO: move to pyelbe.py
@dataclass
class ReferencePoint:
    """
    Class for moment/load reference points

    :param x_coord: x coordinate of the point of reference of the force
    :type x_coord: float
    :param y_coord: y coordinate of the point of reference of the force
    :type y_coord: float
    :param z_coord: z coordinate of the point of reference of the force
    :type z_coord: float

    """

    name: str
    x_coord: float
    y_coord: float
    z_coord: float
    namedtuple: namedtuple = None

    def __post_init__(self):
        """
        Post initialization of reference point

        """
        self.namedtuple = namedtuple(
            self.name,
            [
                "x_coord",
                "y_coord",
                "z_coord",
            ],
        )
        self.namedtuple = (
            self.x_coord,
            self.y_coord,
            self.z_coord,
        )