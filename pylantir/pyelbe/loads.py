"""Loads Classes"""
from dataclasses import dataclass, field
from collections import namedtuple



#TODO: make class LOADS
# make it combination of F, M , points, so we cna translate rotate etc.

#TODO: move to pyelbe.py
@dataclass
class Forces:
    """
    Class for forces

    :param force_x: force in the x direction
    :type force_x: float
    :param force_y: force in the y direction
    :type force_y: float
    :param force_z: force in the z direction
    :type force_z: float

    """

    name: str
    force_x: float
    force_y: float
    force_z: float
    namedtuple: namedtuple = None
    # TODO: add application point?

    def __post_init__(self):
        """
        Post initialization of forces
        """
        self.namedtuple = namedtuple(
            self.name,
            [
                "force_x",
                "force_y",
                "force_z",
            ],
        )
        self.namedtuple = (
            self.force_x,
            self.force_y,
            self.force_z,
        )

#TODO: move to pyelbe.py
@dataclass
class Moments:
    """
    Class for moments

    :param moment_x: moment of the force about the point of application in the x direction
    :type moment_x: float
    :param moment_y: moment of the force about the point of application in the y direction
    :type moment_y: float
    :param moment_z: moment of the force about the point of application in the z direction
    :type moment_z: float

    """

    name: str
    moment_x: float
    moment_y: float
    moment_z: float
    namedtuple: namedtuple = None
    # TODO: add application point?

    def __post_init__(self):
        """
        Post initialization of moments
        """
        self.namedtuple = namedtuple(
            self.name,
            [
                "moment_x",
                "moment_y",
                "moment_z",
            ],
        )
        self.namedtuple = (
            self.moment_x,
            self.moment_y,
            self.moment_z,
        )

