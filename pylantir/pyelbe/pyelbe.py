"""Alles suedlich der Elbe ist Nord-Italien."""

""" profiles """
import logging
import math
from math import sin, cos, radians, pi
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Wedge, Rectangle
from matplotlib.collections import PatchCollection
from dataclasses import KW_ONLY, dataclass, field
from pylantir.scrolls import get_logger
from pylantir.taters import get_markdown_from_docs

logger = get_logger(__name__)


# pylint: disable=C0415, C0103
"""
Library containing general functions and classes for the pyELBE stress Toolkit
"""
from dataclasses import dataclass, field
import matplotlib.pyplot as plt
from matplotlib.patches import Wedge, Rectangle
from matplotlib.collections import PatchCollection
import numpy as np
import pandas as pd

# subel as dataclass
@dataclass
class SubEl:
    """
    Class definition for sub-elements. Used in cross-section definition.


    """

    sub_type: str = ""
    position: tuple = field(default=None)
    pos_x: float = field(default=None)
    pos_y: float = field(default=None)
    fc: str = field(default="tab=blue")
    material: str = field(default=None)

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

        if kwargs.get("fc"):
            self.fc = kwargs.get("fc")

        if kwargs.get("material") is not None:
            self.material = kwargs.get("material")


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

        self.xcg = self.calc_xcg_rect()
        self.ycg = self.calc_ycg_rect()
        self.area = self.calc_area_rect()
        self.Ixx = self.calc_Ixx_rect()
        self.Iyy = self.calc_Iyy_rect()
        self.alpha = radians(self.angle)

    def calc_xcg_rect(self):
        """Calculate the x-coordinate of the center of gravity of the sub-element"""
        if self.angle == 0:
            return self.pos_x + self.width / 2
        else:
            return (
                self.pos_x
                + cos(self.alpha) * (self.width / 2)
                + sin(self.alpha) * (self.height / 2)
            )

    def calc_ycg_rect(self):
        """Calculate the y-coordinate of the center of gravity of the sub-element"""
        if self.angle == 0:
            return self.pos_y + self.height / 2
        else:
            return (
                self.pos_y
                + cos(self.alpha) * (self.height / 2)
                - sin(self.alpha) * (self.width / 2)
            )

    def calc_area_rect(self):
        """Calculate the area of the sub-element"""
        return self.width * self.height

    def calc_Ixx_rect(self):
        """Calculate the moment of inertia of the sub-element around the x-axis"""
        if self.angle == 0:
            return self.width * self.height**3 / 12
        else:
            (self.Ixx + self.Iyy) / 2 + cos(2 * self.alpha) * (self.Ixx - self.Iyy) / 2

    def calc_Iyy_rect(self):
        """Calculate the moment of inertia of the sub-element around the y-axis"""
        if self.angle == 0:
            return self.height * self.width**3 / 12
        else:
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

    def __init__(self, radius, angle, start_angle=0, **kwargs):
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
        super().__init__(sub_type="Arc",**kwargs)

        self.radius = radius
        self.angle = angle
        self.start_angle = start_angle

        self.xcg = self.calc_xcg_arc()
        self.ycg = self.calc_ycg_arc()
        self.area = self.calc_area_arc()
        self.Ixx = self.calc_Ixx_arc()
        self.Iyy = self.calc_Iyy_arc()

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
    :param material: Material of the sub-element. Should be an object from the pyelbe.material_data
    function.
    :type material: object, optional

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
        self.xcg = self.calculate_xcg_fillet()
        self.ycg = self.calculate_ycg_fillet()
        self.radius = radius
        self.area = self.calculate_area_fillet()
        self.Ixx = self.calculate_Ixx_fillet()
        self.Iyy = self.Ixx
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
        # return (16 - 5 * pi) / 16 * self.radius**4
        return 0

    def calculate_Ixy_fillet(self):
        """Calculate the moment of inertia of the sub-element around the xy-axis"""
        # return (19 - 6 * pi) / 24 * self.radius**4
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
    based on the 1st quadrant of the circle (top-right)

    :param fc: Color for the matplotlib representation of the sub-element, should match matplotlib
    color list.
    :type fc: str,optional
    :param material: Material of the sub-element. Should be an object from the pyelbe.material_data
    function.
    :type material: object, optional

    """

    def __init__(self, outer_radius, inner_radius, beta, **kwargs):
        """Init function for auarter-arced sub-class

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
        self.alpha = 45
        self.outer_radius = outer_radius
        self.inner_radius = inner_radius
        self.beta = beta
        self.xcg = self.calculate_xcg_qarc()
        self.ycg = self.calculate_ycg_qarc()
        self.area = self.calculate_area_qarc()
        self.Ixx = self.calculate_Ixx_qarc()
        self.Iyy = self.calculate_Iyy_qarc()

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
        if not self.subel_list:
            self.x_cg = 0
            self.y_cg = 0
            self.area = 0
            self.Ix = 0
            self.Iy = 0
            self.mat_list = []
            self.EA = 0
            self.EIx = 0
            self.EIy = 0
        else:
            
            # self.subel_list = subel_list
            self.area = self.calculate_area()
            self.x_cg = self.calculate_xcg()
            self.y_cg = self.calculate_ycg()
            self.Ix = self.calculate_Ix()
            self.Iy = self.calculate_Iy()

            # if different materials are used, the mechanical values are recalculated according to the
            # material density
            mat_list = [
                subel.material for subel in self.subel_list if subel.material is not None
            ]
            # for subelement in subel_list:
            #    mat_list.append(len(subelement.material))
            # TODO: marry with the Matreel library

            try:
                if 0 not in mat_list:
                    self.EA = (
                        round(sum(i.material[5] * i.area for i in self.subel_list) * 100)
                        / 100
                    )
                    self.x_cg = (
                        round(
                            sum(i.material[5] * i.area * i.xcg for i in self.subel_list)
                            * 100
                            / self.EA
                        )
                        / 100
                    )
                    self.y_cg = (
                        round(
                            sum(i.material[5] * i.area * i.ycg for i in self.subel_list)
                            * 100
                            / self.EA
                        )
                        / 100
                    )
                    self.EIx = int(
                        sum(
                            i.material[5] * (i.Ixx + i.area * (i.ycg - self.y_cg) ** 2)
                            for i in self.subel_list
                        )
                    )
                    self.EIy = int(
                        sum(
                            i.material[5] * (i.Iyy + i.area * (i.xcg - self.x_cg) ** 2)
                            for i in self.subel_list
                        )
                    )
                    self.Ix = int(self.EIx / (self.EA / self.area))
                    self.Iy = int(self.EIy / (self.EA / self.area))
            except IndexError:
                logger.info("No material defined for sub-elements")

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

        return int(
            sum(i.Ixx + i.area * (i.ycg - self.y_cg) ** 2 for i in self.subel_list)
        )

    def calculate_Iy(self):
        """Calculate the moment of inertia of the profile around the y-axis"""

        return int(
            sum(i.Iyy + i.area * (i.xcg - self.x_cg) ** 2 for i in self.subel_list)
        )

@dataclass
class LProfile:
    """Profile class for an L profile.

    :param b: width of the profile
    :type b: float
    :param h: height of the profile
    :type h: float
    :param profile_type: type of profile ("extruded" or "bended")
    :type profile_type: str
    :param t_fx: thickness of the horizontal flange
    :type t_fx: float
    :param t_fy: thickness of the vertical flange (=equal to t_fx with bended profiles)
    :type t_fy: float
    :param r: radius of the fillets / qarc
    :type r: float
    :param mat: material of the profile
    :type mat: list
    :param x: x-coordinate of origin of the profile
    :type x: float
    :param y: y-coordinate of origin of the profile
    :type y: float

    """

    b: float
    h: float
    profile_type: str
    t_fx: float
    t_fy: float = field(default=None)
    r: float = field(default=None)
    mat: list = field(default="dummy")
    x_orig: float = field(default=0)
    y_orig: float = field(default=0)
    
    def __post_init__(self, *args, **kwargs):
        """Init function for LProfile class"""

        if self.profile_type == "extruded":
            self.t_fy = self.t_fy
        elif self.profile_type == "bended":
            self.t_fy = self.t_fx

        if self.r is None and self.profile_type == "bended":
            logging.warning(
                "No radius defined for bended profile, radius is set to 2 t"
            )
            self.r = 2 * self.t_fx

        if self.r is None and self.profile_type == "extruded":
            logging.warning(
                "No radius defined for extruded profile, radius is set to 2 * t_fx"
            )
            self.r = 2 * self.t_fx

        self.subel_list = self.create_subel_list()

        #super().__init__(self.subel_list)
        self.profile = Profile(self.subel_list)

    def create_subel_list(self):
        """Create a list of sub-elements for the profile

        :return: list of sub-elements
        :rtype: list
        """
        subel_list = []

        if self.profile_type == "extruded":
            # build up list from 2 rect and 1 fillet
            subel_list.append(
                Rect(
                    width=self.b,
                    height=self.t_fx,
                    pos_x=self.x_orig + self.b / 2,
                    pos_y=self.y_orig + self.t_fx / 2,
                    material=self.mat,
                    angle=0,
                )
            )

            subel_list.append(
                Rect(
                    width=self.t_fy,
                    height=self.h,
                    pos_x=self.x_orig + self.t_fy / 2,
                    pos_y=self.y_orig - self.h / 2,
                    material=self.mat,
                    angle=0,
                )
            )
            subel_list.append(
                Fillet(
                    width=self.t_fx,
                    height=self.h - 2 * self.t_fx,
                    pos_x=self.x_orig + self.b / 2,
                    pos_y=self.y_orig,
                    material=self.mat,
                    angle=0,
                    r=self.r,
                )
            )

        elif self.profile_type == "bended":
            # build up list from 2 rect and 1 qarc
            
            subel_list.append(
                Rect(
                    width=self.b - self.t_fy - self.r,
                    height=self.t_fx,
                    pos_x=self.x_orig + self.t_fx / 2,
                    pos_y=self.y_orig + self.t_fy + self.r + ((self.b - self.t_fy - self.r) / 2),
                    material=self.mat,
                    angle=0,
                )
            )
            subel_list.append(
                Rect(
                    width=self.t_fy,
                    height=self.h - self.t_fx - self.r,
                    pos_x=self.x_orig + self.t_fy / 2,
                    pos_y=self.y_orig + self.t_fx + self.r + ((self.h - self.t_fx - self.r) / 2),
                    material=self.mat,
                    angle=0,
                )
            )
            subel_list.append(
                QArc(
                    outer_radius=self.r + self.t_fx,
                    inner_radius=self.r,
                    pos_x=self.x_orig + self.t_fy + self.r,
                    pos_y=self.y_orig + self.t_fx + self.r,
                    material=self.mat,
                    beta=90               
                )
            )

        return subel_list
    
    def get_profile(self):
        return self.profile

    @property
    def area(self):
        """Area of the profile"""
        return self.profile.area
    
    @property
    def x_cg(self):
        """x-coordinate of the center of gravity of the profile"""
        return self.profile.x_cg
    
    @property
    def y_cg(self):
        """y-coordinate of the center of gravity of the profile"""
        return self.profile.y_cg
    
    @property
    def Ixx(self):
        """Moment of inertia of the profile around the x-axis"""
        return self.profile.Ixx
    
    @property
    def Iyy(self):
        """Moment of inertia of the profile around the y-axis"""
        return self.profile.Iyy
    
    @property
    def Ixy(self):
        """Moment of inertia of the profile around the xy-axis"""
        return self.profile.Ixy
    
    