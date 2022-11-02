#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Helper functions for geometry calculations
"""
from array import array
from collections import namedtuple
from math import cos, radians, sin, pi
from sys import flags
import numpy as np
from pylantir.scrolls import get_logger

# logger
logger = get_logger(__name__)

# area of rectangle
def area_rectangle(width: float, height: float) -> float:
    """Calculate the area of a rectangle

    :param width: Width of the rectangle
    :type width: float
    :param height: Height of the rectangle
    :type height: float
    :return: Area of the rectangle
    :rtype: float
    """
    return width * height


# centroid of rectangle
def centroid_rectangle(width: float, height: float, angle: float = 0) -> array:
    """Calculate the centroid of a rectangle relative to 0, 0

    :param width: Width of the rectangle
    :type width: float
    :param height: Height of the rectangle
    :type height: float
    :param angle: Angle of the rectangle, degrees
    :type angle: float
    :return: Centroid of the rectangle
    :rtype: tuple
    """
    # if rectangle was on x axis
    C = [width / 2, height / 2]
    # rotate centroid to correct position
    logger.debug("Angle: %s °", angle)
    angle = radians(angle)
    logger.debug("angle: %s rad", angle)
    logger.debug("C: %s", C)
    C = np.dot(np.array([[cos(angle), -sin(angle)], [sin(angle), cos(angle)]]), C)
    logger.debug("C: %s", C)
    # make namedtuples
    Cx = C[0]
    Cy = C[1]
    C = namedtuple("C", ["Cx", "Cy"])
    C = C(Cx, Cy)
    logger.debug("C: %s", C)
    return C


# Inertia of rectangle
# def inertia_rectangle(width, height, angle):
def inertia_rectangle(width: float, height: float, angle: float = 0) -> tuple:
    """Calculate the inertia of a rectangle

    :param width: Width of the rectangle
    :type width: float
    :param height: Height of the rectangle
    :type height: float
    :param angle: Angle of the rectangle, degrees
    :type angle: float
    :return: Inertia of the rectangle
    :rtype: tuple
    """
    # if rectangle was on x axis
    Ix = height**3 * width / 12
    Iy = width**3 * height / 12
    Ixy = 0

    if angle:
        Ix, Iy, Ixy = rotate_inertia(Ix, Iy, Ixy, angle)
        # rotate inertia to correct position
        # bh/12 (h**2 cos(angle)**2 + b**2 sin(angle)**2)
        # Ix = ((height * width) / 12) * (
        #    width * cos(radians(angle)) ** 2 + sin(radians(angle)) ** 2
        # )
        # Iy = ((height * width) / 12) * (
        #    height * cos(radians(angle)) ** 2 + sin(radians(angle)) ** 2
        # )

    logger.debug("Ix: %s", Ix)
    logger.debug("Iy: %s", Iy)
    # rotate inertia to correct position
    # Ix = Ix + A * Cy**2
    # Iy = Iy + A * Cx**2
    # angle = radians(angle)#
    # logger.debug("angle: %s rad", angle)
    # area_rect = area_rectangle(width, height)
    # logger.debug("area_rect: %s", area_rect)
    # Cx, Cy = centroid_rectangle(width, height, angle)
    # logger.debug("Cx: %s", Cx)
    # logger.debug("Cy: %s", Cy)
    # Ix = Ix + area_rect * Cy**2
    # logger.debug("Ix: %s", Ix)
    # Iy = Iy + area_rect * Cx**2
    # logger.debug("Iy: %s", Iy)

    return Ix, Iy


def translate_inertia(Inertia: float, area: float, cg: float, ref: float = 0) -> float:
    """Translate inertia to a new reference point

    :param Inertia: Inertia of the object
    :type Inertia: float
    :param area: Area of the object
    :type area: float
    :param cg: Center of gravity of the object
    :type cg: float
    :param ref: Reference point
    :type ref: float
    :return: Inertia of the object at the new reference point
    :rtype: float
    """
    return Inertia + area * (cg - ref) ** 2


def rotate_inertia(Ixg: float, Iyg: float, Ixy: float, angle: float) -> tuple:
    """Rotate inertia

    :param Ixg: Inertia around x axis
    :type Ixg: float
    :param Iyg: Inertia around y axis
    :type Iyg: float
    :param angle: Angle of rotation, degrees
    :type angle: float
    :return: Inertia around x and y axis
    :rtype: tuple
    """
    angle = radians(angle)
    logger.debug("angle: %s rad", angle)
    Iu = (Ixg + Iyg) / 2 + ((Ixg - Iyg) / 2) * cos(2 * angle) + Ixy * sin(2 * angle)
    logger.debug("Iu: %s", Iu)
    Iv = (Ixg + Iyg) / 2 - ((Ixg - Iyg) / 2) * cos(2 * angle) - Ixy * sin(2 * angle)
    logger.debug("Iv: %s", Iv)
    Iuv = (Ixg - Iyg) / 2 * sin(2 * angle) + Ixy * cos(2 * angle)
    logger.debug("Iuv: %s", Iuv)

    return Iu, Iv, Iuv


def area_circle_sector(
    radius: float, start_angle: float = 0, end_angle: float = 360
) -> float:
    """Calculate the area of a circle segment, default is a full circle

    :param radius: Radius of the circle segment
    :type radius: float
    :param start_angle: Start angle of the circle segment, degrees
    :type start_angle: float
    :param end_angle: End angle of the circle segment, degrees
    :type end_angle: float
    :return: Area of the circle segment
    :rtype: float
    """
    return 0.5 * radius**2 * (radians(end_angle - start_angle))


# area of arc segment
def area_arc_sector(
    radius: float, thickness: float, start_angle: float = 0, end_angle: float = 360
) -> float:
    """Calculate the area of an arc segment, default is a hollow circle

    :param radius: Radius of the arc segment
    :type radius: float
    :param thickness: Thickness of the arc segment
    :type thickness: float
    :param start_angle: Start angle of the arc segment, degrees
    :type start_angle: float
    :param end_angle: End angle of the arc segment, degrees
    :type end_angle: float
    :return: Area of the arc segment
    :rtype: float
    """
    # check if inner radius is smaller than outer radius
    # if radius < thickness:
    #    raise ValueError("Inner radius is smaller than outer radius")

    outer_circle = area_circle_sector(radius + thickness, start_angle, end_angle)
    inner_circle = area_circle_sector(radius, start_angle, end_angle)

    return abs(outer_circle - inner_circle)


# centroid of circle segment
def centroid_circle_sector(
    radius: float, start_angle: float, end_angle: float
) -> tuple:
    """Calculate the centroid of a circle segment

    :param radius: Radius of the circle segment
    :type radius: float
    :param start_angle: Start angle of the circle segment, degrees
    :type start_angle: float
    :param end_angle: End angle of the circle segment, degrees
    :type end_angle: float
    :return: Centroid of the circle segment
    :rtype: tuple
    """
    # if sector was on x axis

    Cx = (
        2
        * radius
        * sin(radians((end_angle - start_angle) / 2))
        / (3 * radians((end_angle - start_angle) / 2))
    )
    logger.debug("Cx: %s", Cx)
    Cy = 0
    logger.debug("Cy: %s", Cy)

    # rotate centroid to correct position
    logger.debug("start_angle: %s", start_angle)
    logger.debug("end_angle: %s", end_angle)
    angle = radians(start_angle + (end_angle - start_angle) / 2)
    logger.debug("angle: %s rad", angle)
    logger.debug("Cos: %s", cos(angle))
    logger.debug("Sin: %s", sin(angle))
    Cx_rotated = Cx * cos(angle) - Cy * sin(angle)
    logger.debug("Cx: %s", Cx_rotated)
    Cy_rotated = Cx * sin(angle) + Cy * cos(angle)
    logger.debug("Cy: %s", Cy_rotated)

    return Cx_rotated, Cy_rotated


# centroid of arc segment
def centroid_arc_sector(
    radius: float, thickness: float, start_angle: float, end_angle: float
) -> tuple:
    """Calculate the centroid of an arc segment

    :param radius: Radius of the arc segment
    :type radius: float
    :param thickness: Thickness of the arc segment
    :type thickness: float
    :param start_angle: Start angle of the arc segment, degrees
    :type start_angle: float
    :param end_angle: End angle of the arc segment, degrees
    :type end_angle: float
    :return: Centroid of the arc segment
    :rtype: tuple
    """
    # if sector was on x axis
    logger.debug("radius: %s", radius)
    logger.debug("thickness: %s", thickness)
    logger.debug("start_angle: %s", start_angle)
    logger.debug("end_angle: %s", end_angle)

    alpha = radians((end_angle - start_angle) / 2)
    logger.debug("alpha: %s", alpha)
    radius_1 = radius
    radius_2 = radius + thickness

    Cx = ((2 * sin(alpha)) / (3 * alpha)) * (
        (radius_2**3 - radius_1**3) / (radius_2**2 - radius_1**2)
    )
    logger.debug("Cx: %s", Cx)
    Cy = 0
    # rotate centroid to correct position
    angle = radians(start_angle + (end_angle - start_angle) / 2)
    logger.debug("angle: %s rad", angle)
    Cx_rotated = Cx * cos(angle) - Cy * sin(angle)
    logger.debug("Cx: %s", Cx_rotated)
    Cy_rotated = Cx * sin(angle) + Cy * cos(angle)
    logger.debug("Cy: %s", Cy_rotated)

    return Cx_rotated, Cy_rotated


# Inertia of circle segment
def inertia_circle_sector(
    radius: float, start_angle: float, end_angle: float, cg: bool = True
) -> tuple:
    """Calculate the inertia of a circle segment

    :param radius: Radius of the circle segment
    :type radius: float
    :param start_angle: Start angle of the circle segment, degrees
    :type start_angle: float
    :param end_angle: End angle of the circle segment, degrees
    :type end_angle: float
    :return: Inertia of the circle segment
    :rtype: tuple
    :param cg: If True, return the inertia of the circle segment with respect to the centroid, else in circle center
    :type cg: bool
    """
    # in sector centroid
    Ix = Iy = (1 / 8) * radius**4 * (radians(end_angle - start_angle))
    Ixy = 0

    if not cg:
        # in circle center
        # centroid of circle segment
        Cx, Cy = centroid_circle_sector(radius, start_angle, end_angle)
        logger.debug("Cx: %s", Cx)
        logger.debug("Cy: %s", Cy)

        area = area_circle_sector(radius, start_angle, end_angle)
        logger.debug("area: %s", area)
        # inertia of circle segment with respect to centroid

        Ix = Ix + area * Cy**2

        Iy = Iy + area * Cx**2
        Ixy = Ixy + area_circle_sector(radius, start_angle, end_angle) * Cy * Cx

    return Ix, Iy, Ixy


# Inertia of arc segment
def inertia_arc_sector(
    radius: float,
    thickness: float,
    start_angle: float,
    end_angle: float,
    cg: bool = False,
) -> tuple:
    """Calculate the inertia of an arc segment

    :param radius: Radius of the arc segment
    :type radius: float
    :param thickness: Thickness of the arc segment
    :type thickness: float
    :param start_angle: Start angle of the arc segment, degrees
    :type start_angle: float
    :param end_angle: End angle of the arc segment, degrees
    :type end_angle: float
    :return: Inertia of the arc segment
    :rtype: float
    :param cg: If True, return the inertia of the arc segment with respect to the centroid, else in circle center
    :type cg: bool
    """
    # todo: 0 ≤ alpha ≤ 2pi
    # in sector centroid
    # logger.debug("radius: %s", radius)
    # circle_part = (radians(end_angle) - radians(start_angle)) / (2 * pi)
    # logger.debug("circle_part: %s", circle_part)
    # I_circle_1 = (1 / 4) * pi * (radius + thickness) ** 4
    # logger.debug("I_circle_1: %s", I_circle_1)
    # I_circle_2 = (1 / 4) * pi * radius**4
    # logger.debug("I_circle_2: %s", I_circle_2)
    # Ix = Iy = circle_part * (I_circle_1 - I_circle_2)
    #

    Ix_sector_1, Iy_sector_1, Ixy_sector_1 = inertia_circle_sector(
        radius, start_angle, end_angle, False
    )
    logger.debug("Ix_sector_1: %s", Ix_sector_1)
    Ix_sector_2, Iy_sector_2, Ixy_sector_2 = inertia_circle_sector(
        radius + thickness, start_angle, end_angle, False
    )
    logger.debug("Ix_sector_2: %s", Ix_sector_2)

    Ix = Ix_sector_2 - Ix_sector_1

    Iy = Iy_sector_2 - Iy_sector_1

    Ixy = Ixy_sector_2 - Ixy_sector_1

    if cg:
        # in circle center
        # centroid of arc segment
        Cx, Cy = centroid_arc_sector(radius, thickness, start_angle, end_angle)
        logger.debug("Cx: %s", Cx)
        logger.debug("Cy: %s", Cy)

        area = area_arc_sector(radius, thickness, start_angle, end_angle)
        logger.debug("area: %s", area)
        # inertia of arc segment with respect to centroid

        Ix = Ix + area * Cy**2

        Iy = Iy + area * Cx**2
        Ixy = Ixy + area * Cy * Cx

    return Ix, Iy, Ixy
