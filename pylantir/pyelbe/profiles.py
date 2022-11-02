""" profiles """
import logging
import math
from math import sin, cos, radians, pi
from unicodedata import name
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Wedge, Rectangle
from matplotlib.collections import PatchCollection
import numpy as np
from dataclasses import KW_ONLY, dataclass, field
from pylantir.scrolls import get_logger
from pylantir.taters import get_markdown_from_docs
from pylantir.pyweser.matreel.material import Material

from .geometry_helpers import (
    area_arc_sector,
    area_circle_sector,
    area_rectangle,
    centroid_arc_sector,
    centroid_circle_sector,
    centroid_rectangle,
    inertia_arc_sector,
    inertia_circle_sector,
    inertia_rectangle,
    translate_inertia,
)

logger = get_logger(__name__)


# pylint: disable=C0415, C0103
"""
Library containing general functions and classes for the pyELBE stress Toolkit
"""

# subel as dataclass
@dataclass
class SubEl:
    """
    Class definition for sub-elements. Used in cross-section definition.

    :param name: name of the sub-element
    :type name: str
    :param position: position of the sub-element
    :type position: tuple
    :param pos_x: x-position of the sub-element
    :type pos_x: float
    :param pos_y: y-position of the sub-element
    :type pos_y: float
    :param mat_name: name of the material
    :type mat_name: str
    :param mat_spec: specification of the material
    :type mat_spec: str
    :param fc: facecolor of the sub-element
    :type fc: str

    """

    name: str = None
    sub_type: str = ""
    position: tuple = field(default=None)
    pos_x: float = field(default=None)
    pos_y: float = field(default=None)
    fc: str = field(default="blue")
    mat_name: str = field(default=None)
    mat_spec: str = field(default=None)
    material: Material = field(default=None)

    def __post_init__(self, **kwargs):
        # check if either position or pos_x and pos_y are defined
        if self.position is None and (self.pos_x is None or self.pos_y is None):
            raise ValueError("Either position or pos_x and pos_y must be defined")

        # if position is defined, set pos_x and pos_y
        if self.position is not None:
            self.pos_x = self.position[0]
            self.pos_y = self.position[1]

        # if pos_x and pos_y are defined, set position
        if self.pos_x is not None and self.pos_y is not None:
            self.position = (self.pos_x, self.pos_y)

        if self.mat_name is not None:
            if self.mat_spec is not None:
                self.material = Material(
                    name=self.mat_name, specification=self.mat_spec
                )
            else:
                logger.warning(
                    f"{self.name}: For material definition, both name and spec are needed"
                )


@dataclass
class Rect(SubEl):
    """
    Sub-class definition for rectangular-shaped sub-elements. Used in cross-section definition.
    Origin point for this sub-element is the lower left point of the rectangle.

    :param width: Width of the rectangle
    :type width: float
    :param height: Height of the rectangle
    :type height: float
    :param angle: Angle of the rectangle in degrees
    :type angle: float

    """

    def __init__(self, width, height, angle=0, sub_type="Rect", **kwargs):
        """
        Init function for Rect sub-class

        :param xcg: x-coordinate of the center of gravity of the sub-element
        :type xcg: float
        :param ycg: y-coordinate of the center of gravity of the sub-element
        :type ycg: float
        :param area: Area of the sub-element
        :type area: float
        :param Ixx: Moment of inertia of the sub-element around the x-axis
        :type Ixx: float
        :param Iyy: Moment of inertia of the sub-element around the y-axis
        :type Iyy: float

        """
        super().__init__(sub_type=sub_type, **kwargs)

        self.width = width
        self.height = height
        self.angle = angle

        self.alpha = radians(self.angle)
        # self.xcg = self.calc_xcg_rect()
        # self.ycg = self.calc_ycg_rect()
        self.xcg, self.ycg = centroid_rectangle(
            width=self.width, height=self.height, angle=self.angle
        )
        self.xcg += self.pos_x
        self.ycg += self.pos_y

        self.area = area_rectangle(
            width=self.width, height=self.height
        )  # self.calc_area_rect()
        self.Ixg, self.Iyg = inertia_rectangle(
            width=self.width, height=self.height, angle=self.angle
        )

        # self.calc_Ixx_rect()
        # self.Iyy = self.calc_Iyy_rect()
        # if self.angle != 0:
        #   self.Ixx_rotated = self.calc_Ixx_rect_rotated()
        #   self.Iyy_rotated = self.calc_Iyy_rect_rotated()

    def calc_Ixx_rect_rotated(self):
        """Calculate the moment of inertia of the sub-element around the x-axis, rotated with alpha"""
        return (self.Ixx + self.Iyy) / 2 + cos(2 * self.alpha) * (
            self.Ixx - self.Iyy
        ) / 2

    def calc_Iyy_rect_rotated(self):
        """Calculate the moment of inertia of the sub-element around the y-axis, rotated with alpha"""
        (self.Ixx + self.Iyy) / 2 - cos(2 * self.alpha) * (self.Ixx - self.Iyy) / 2


@dataclass
class Arc(SubEl):
    """
    Sub-class definition for arc-shaped sub-elements. Used in cross-section definition.
    Origin point for this sub-element is the center of the arc.

    :param outer_radius: Outer radius of the sub-element
    :type outer_radius: float
    :param inner_radius: Inner radius of the sub-element
    :type inner_radius: float
    :param angle: Angle of the arc in degrees
    :type angle: float
    :param start_angle: Start angle of the arc in degrees
    :type start_angle: float
    """

    def __init__(self, outer_radius, inner_radius, angle=180, start_angle=0, **kwargs):
        """
        Init function for Arc sub-class

        :param xcg: x-coordinate of the center of gravity of the sub-element
        :type xcg: float
        :param ycg: y-coordinate of the center of gravity of the sub-element
        :type ycg: float
        :param area: Area of the sub-element
        :type area: float
        :param Ixx: Moment of inertia of the sub-element around the x-axis
        :type Ixx: float
        :param Iyy: Moment of inertia of the sub-element around the y-axis
        :type Iyy: float

        """
        super().__init__(sub_type="Arc", **kwargs)

        self.radius = inner_radius
        self.outer_radius = outer_radius
        self.inner_radius = inner_radius

        self.angle = angle
        self.start_angle = start_angle
        self.end_angle = self.start_angle + self.angle

        self.thickness = self.outer_radius - self.inner_radius

        logger.debug(f"{self.name}: start_angle = {self.start_angle}")
        logger.debug(f"{self.name}: end_angle = {self.end_angle}")

        self.area = area_arc_sector(
            radius=self.radius,
            thickness=self.thickness,
            start_angle=self.start_angle,
            end_angle=self.end_angle,
        )  # self.calc_area_arc()

        self.xcg, self.ycg = centroid_arc_sector(
            radius=self.radius,
            thickness=self.thickness,
            start_angle=self.start_angle,
            end_angle=self.end_angle,
        )  # self.calc_xcg_arc()

        self.Ixg, self.Iyg = inertia_arc_sector(
            radius=self.radius,
            thickness=self.thickness,
            start_angle=self.start_angle,
            end_angle=self.end_angle,
        )

        # self.Iyy = self.calc_Iyy_arc()

    def calc_xcg_arc(self):
        """Calculate the x-coordinate of the center of gravity of the sub-element"""
        return self.pos_x

    def calc_ycg_arc(self):
        """Calculate the y-coordinate of the center of gravity of the sub-element"""
        return self.pos_y + (1.333 / pi) * (
            self.outer_radius**3 - self.inner_radius**3
        ) / (self.outer_radius**2 - self.inner_radius**2)

    def calc_area_arc(self):
        """Calculate the area of the sub-element"""
        return pi / 2 * (self.outer_radius**2 - self.inner_radius**2)

    def calc_Ixx_arc(self):
        """Calculate the moment of inertia of the sub-element around the x-axis"""
        return (9 * pi**2 - 64) * (
            self.outer_radius**4 - self.inner_radius**4
        ) / (72 * pi) + pi / 2 * (
            self.outer_radius**2
            * (1.333 / pi * self.outer_radius - self.ycg + self.pos_y) ** 2
            - self.inner_radius**2
            * (1.333 / pi * self.inner_radius - self.ycg + self.pos_y) ** 2
        )

    def calc_Iyy_arc(self):
        "Calculate the moment of inertia of the sub-element around the y-axis"
        return (pi / 8) * (self.outer_radius**4 - self.inner_radius**4)


class Fillet(SubEl):
    """Sub-class definition for fillet sub-elements. Used in cross-section definition.

    :param pos_x: x-coordinate of the center of the fillet
    :type pos_x: float
    :param pos_y: y-coordinate of the center of the fillet
    :type pos_y: float
    :param radius: Radius of the fillet
    :type radius: float

    :param fc: Color for the matplotlib representation of the sub-element, should match matplotlib
        color list.
    :type fc: str,optional

    """

    def __init__(self, radius, **kwargs):
        """Init function for Fillet sub-class

        :param xcg: x-coordinate of the center of gravity of the sub-element
        :type xcg: float
        :param ycg: y-coordinate of the center of gravity of the sub-element
        :type ycg: float
        :param area: Area of the sub-element
        :type area: float
        :param Ixx: Moment of inertia of the sub-element around the x-axis. For simplicity the
        moment of inertia around the x-axis is set to 0.
        :type Ixx: float
        :param Iyy: Moment of inertia of the sub-element around the y-axis. For simplicity the
        moment of inertia around the x-axis is set to 0.
        :type Iyy: float
        :param Ixy: Moment of inertia of the sub-element around the xy-axis
        :type Ixy: float

        """
        super().__init__(sub_type="Fillet", **kwargs)
        self.radius = radius
        # @properties?
        self.xcg = self.calculate_xcg_fillet()
        self.ycg = self.calculate_ycg_fillet()

        self.area = self.calculate_area_fillet()
        self.Ixg = self.calculate_Ixx_fillet()
        self.Iyg = self.Ixg
        self.Ixy = self.calculate_Ixy_fillet()

    def calculate_xcg_fillet(self):
        """Calculate the x-coordinate of the center of gravity of the sub-element"""
        return self.pos_x + self.radius / 2

    def calculate_ycg_fillet(self):
        """Calculate the y-coordinate of the center of gravity of the sub-element"""
        return self.pos_y + self.radius / 2

    def calculate_area_fillet(self):
        """Calculate the area of the sub-element"""
        return self.radius**2 * (1 - pi / 4)

    def calculate_Ixx_fillet(self):
        """Calculate the moment of inertia of the sub-element around the x-axis"""
        # TODO: inertia of square - circle?
        return 0

    def calculate_Ixy_fillet(self):
        """Calculate the moment of inertia of the sub-element around the xy-axis"""

        return 0


class QArc(SubEl):
    """
    Sub-class definition for quarter-arced shaped sub-elements. Used in cross-section definition.
    Origin point for this sub-element is the center point of the circle defining it.

    :param pos_x: x-coordinate of the origin of the quarter arc
    :type pos_x: float
    :param pos_y: y-coordinate of the origin of the quarter arc
    :type pos_y: float
    :param outer_radius: Radius of the quarter arc
    :type outer_radius: float
    :param inner_radius: Radius of the quarter arc
    :type inner_radius: float
    :param beta: opening angle based from origin point to arc: Example: 45 for a sub-element
    based on the 1st quadrant of the circle (top-right) TODO: discuss meaning with KH

    :param fc: Color for the matplotlib representation of the sub-element, should match matplotlib
    color list.
    :type fc: str,optional
    """

    def __init__(self, outer_radius, inner_radius, beta, **kwargs):
        """Init function for quarter-arced sub-class

        :param xcg: x-coordinate of the center of gravity of the sub-element
        :type xcg: float
        :param ycg: y-coordinate of the center of gravity of the sub-element
        :type ycg: float
        :param area: Area of the sub-element
        :type area: float
        :param Ixx: Moment of inertia of the sub-element around the x-axis. For simplicity the
        moment of inertia around the x-axis is set to 0.
        :type Ixx: float
        :param Iyy: Moment of inertia of the sub-element around the y-axis. For simplicity the
        moment of inertia around the x-axis is set to 0.
        :type Iyy: float

        """
        super().__init__(sub_type="QArc", **kwargs)
        self.alpha = 90
        self.outer_radius = outer_radius
        self.inner_radius = self.radius = inner_radius
        self.thickness = self.outer_radius - self.inner_radius
        self.beta = beta
        self.start_angle = self.beta - 45
        self.end_angle = self.start_angle + self.alpha

        self.area = area_arc_sector(
            radius=self.radius,
            thickness=self.thickness,
            start_angle=self.start_angle,
            end_angle=self.end_angle,
        )
        # self.calculate_area_qarc()

        # self.xcg = self.calculate_xcg_qarc()
        # self.ycg = self.calculate_ycg_qarc()
        self.xcg, self.ycg = centroid_arc_sector(
            radius=self.radius,
            thickness=self.thickness,
            start_angle=self.start_angle,
            end_angle=self.end_angle,
        )
        #self.Ixx = self.calculate_Ixx_qarc()
        #self.Iyy = self.calculate_Iyy_qarc()
        self.Ixx, self.Iyy = inertia_arc_sector(
            radius=self.radius,
            thickness=self.thickness,
            start_angle=self.start_angle,
            end_angle=self.end_angle,
        )

    def calculate_xcg_qarc(self):
        """Calculate the x-coordinate of the center of gravity of the sub-element"""

        return self.pos_x + math.cos(radians(self.beta)) * 0.6667 * math.sin(
            radians(self.alpha)
        ) / radians(self.alpha) * (self.outer_radius**3 - self.inner_radius**3) / (
            self.outer_radius**2 - self.inner_radius**2
        )

    def calculate_ycg_qarc(self):
        """Calculate the y-coordinate of the center of gravity of the sub-element"""

        return self.pos_y + math.sin(radians(self.beta)) * 0.6667 * math.sin(
            radians(self.alpha)
        ) / radians(self.alpha) * (self.outer_radius**3 - self.inner_radius**3) / (
            self.outer_radius**2 - self.inner_radius**2
        )

    def calculate_area_qarc(self):
        """Calculate the area of the sub-element"""

        return radians(self.alpha) * (self.outer_radius**2 - self.inner_radius**2)

    def calculate_Ixx_qarc(self):
        """Calculate the moment of inertia of the sub-element around the x-axis"""

        return (
            radians(self.alpha) / 4 * (self.outer_radius**4 - self.inner_radius**4)
            - self.area * (self.ycg - self.pos_y) ** 2
        )

    def calculate_Iyy_qarc(self):
        """Calculate the moment of inertia of the sub-element around the y-axis"""

        return (
            radians(self.alpha) / 4 * (self.outer_radius**4 - self.inner_radius**4)
            - self.area * (self.xcg - self.pos_x) ** 2
        )


@dataclass
class Profile:
    """
    Profile class combines defined Subels and returns combined mechanical values.
    By using different materials for the subels, the mechanical values are recalculated based on
    the different young moduli.

    Args:
        subel_list (list): List of SubEl objects which describe the profile.

    """

    subel_list: list
    name: str = field(default="Profile")

    def __post_init__(self):
        """Init function for Profile class

        Attributes:
            x_cg: X-coordinate of center of gravity from whole profile
            y_cg: X-coordinate of center of gravity from whole profile
            area: Area of whole profile
            Ix: Moment of inertia of profile around x-axis
            Iy: Moment of inertia of profile around y-axis
            mat_list(optional): If materials are defined in the sub-elements
                                a list of materials is created.
            EA (optional): If materials are used, the sum of the product
                            of the young modulues and the area of each sub-element is given here
            EIx (optional): If materials are used, the sum of the product of the young modulus
                    and the moment if inertia around the x-axis of each sub-element is given here
            EIy (optional): If materials are used, the sum of the product of the young modulus
                    and the moment if inertia around the x-axis of each sub-element is given here

        """
        # if the element list is empty, create an empty profile
        # self.subel_list = subel_list
        self.area = self.calculate_area()
        self.x_cg = self.calculate_xcg()
        self.y_cg = self.calculate_ycg()
        self.Ixg = self.calculate_Ix()
        self.Iyg = self.calculate_Iy()

        # inertia of the profile around the origin
        self.Ixx = translate_inertia(self.Ixg, self.area, self.y_cg)
        self.Iyy = translate_inertia(self.Iyg, self.area, self.x_cg)

        # if different materials are used, the mechanical values are recalculated according to the
        # material density
        self.mat_list = [
            subel.material for subel in self.subel_list if subel.material is not None
        ]
        logging.debug(f"{self.mat_list}")
        # for subelement in subel_list:
        #    mat_list.append(len(subelement.material))
        # TODO: marry with the Matreel library

        self.EA = 0
        # self.x_cg = 0
        # self.y_cg = 0
        self.EIx = 0
        self.EIy = 0
        # self.Ix
        # self.Iy
        # try:
        # if len(self.mat_list) == len(self.subel_list):
        #    self.EA = (
        #        round(sum(i.material[5] * i.area for i in self.subel_list) * 100)
        #        / 100
        #    )
        #    self.x_cg = (
        #        round(
        #            sum(i.material[5] * i.area * i.xcg for i in self.subel_list)
        #            * 100
        #            / self.EA
        #        )
        #        / 100
        #    )
        #    self.y_cg = (
        #        round(
        #            sum(i.material[5] * i.area * i.ycg for i in self.subel_list)
        #            * 100
        #            / self.EA
        #        )
        #        / 100
        #    )
        #    self.EIx = int(
        #        sum(
        #            i.material[5] * (i.Ixx + i.area * (i.ycg - self.y_cg) ** 2)
        #            for i in self.subel_list
        #        )
        #    )
        #    self.EIy = int(
        #        sum(
        #            i.material[5] * (i.Iyy + i.area * (i.xcg - self.x_cg) ** 2)
        #            for i in self.subel_list
        #        )
        #    )
        #    self.Ix = int(self.EIx / (self.EA / self.area))
        #    self.Iy = int(self.EIy / (self.EA / self.area))
        # else:
        #    logger.info("Material not defined for all sub-elements")

    def calculate_area(self):
        """Calculate the area of the profile"""

        return round(sum(i.area for i in self.subel_list) * 100) / 100

    def calculate_xcg(self):
        """Calculate the x-coordinate of the center of gravity of the profile"""

        return (
            round(sum(i.area * i.xcg for i in self.subel_list) * 100 / self.area) / 100
        )

    def calculate_ycg(self):
        """Calculate the y-coordinate of the center of gravity of the profile"""

        return (
            round(sum(i.area * i.ycg for i in self.subel_list) * 100 / self.area) / 100
        )

    def calculate_Ix(self):
        """Calculate the moment of inertia of the profile around the x-axis"""

        return sum(i.Ixg + i.area * (i.ycg - self.y_cg) ** 2 for i in self.subel_list)

    def calculate_Iy(self):
        """Calculate the moment of inertia of the profile around the y-axis"""

        return sum(i.Iyg + i.area * (i.xcg - self.x_cg) ** 2 for i in self.subel_list)
