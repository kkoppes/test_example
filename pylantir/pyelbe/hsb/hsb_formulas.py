#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""supporting functions for the HSB methods"""
from collections import namedtuple
import math
import numpy as np


def moment_x_reference(  # pylint: disable=too-many-arguments
    moment_x_p: float,
    force_y: float,
    force_z: float,
    z_coord_p: float,
    y_coord_p: float,
    z_coord_u: float = 0,
    y_coord_u: float = 0,
) -> float:
    r"""
    Calculates the moment of the force about the point of application in the x direction.
    NOTE: Changed slightly from the HSB to insert absolute coordinates for both applied and
    reference points

    :math:`M_{xU} = M_{xP} - F_{y}\cdot (z_{P} - z_{U}) + F_{z}\cdot (y_{P} - y_{U})`

    :param moment_x_p: moment of the force about the point of application in the x direction
    :type moment_x_p: float
    :param force_y: force in the y direction
    :param force_y: float
    :param force_z: force in the z direction
    :param force_z: float
    :param z_coord_p: z coordinate of the point of application of the force
    :param z_coord_p: float
    :param y_coord_p: y coordinate of the point of application of the force
    :param y_coord_p: float
    :param y_coord_u: y coordinate of the point of reference of the force
    :param y_coord_u: float
    :return moment_mxu: moment of the force about the point of application in the x direction
    :rtype: float

    """

    moment_x_ref = (
        moment_x_p
        - force_y * (z_coord_p - z_coord_u)
        + force_z * (y_coord_p - y_coord_u)
    )
    return float(moment_x_ref)


# markdown of this function above
# pylint: disable=too-many-arguments
def moment_x_reference_markdown(
    moment_x_p: float,
    force_y: float,
    force_z: float,
    z_coord_p: float,
    y_coord_p: float,
    z_coord_u: float = 0,
    y_coord_u: float = 0,
) -> tuple:
    """
    Create markdown in LaTeX for moment_x_reference
    NOTE: Changed slightly from the HSB to insert absolute coordinates for both applied and
    reference points

    :param moment_x_p: moment of the force about the point of application in the x direction
    :type moment_x_p: float
    :param force_y: force in the y direction
    :param force_y: float
    :param force_z: force in the z direction
    :param force_z: float
    :param z_coord_p: z coordinate of the point of application of the force
    :param z_coord_p: float
    :param y_coord_p: y coordinate of the point of application of the force
    :param y_coord_p: float
    :param y_coord_u: y coordinate of the point of reference of the force
    :param y_coord_u: float
    :return markdown: markdown in LaTeX for moment_x_reference
    :rtype: str

    """

    moment_x_ref = moment_x_reference(
        moment_x_p, force_y, force_z, z_coord_p, y_coord_p, z_coord_u, y_coord_u
    )
    # for LaTeX
    # pylint: disable=anomalous-backslash-in-string
    markdown_formula = r"""$$
    M_{xU} = M_{xP} - F_{y}\cdot (z_{P} - z_{U}) + F_{z}\cdot (y_{P} - y_{U})
    $$

    """
    markdown_filled = (
        f"$${moment_x_ref} = "
        f"{moment_x_p} - {force_y} "
        r"\cdot "
        f"({z_coord_p} - {z_coord_u}) + "
        f"{force_z} "
        r"\cdot "
        f"({y_coord_p} - {y_coord_u})$$"
    )
    # pylint: enable=anomalous-backslash-in-string
    return (markdown_formula, markdown_filled)


# pylint: disable=too-many-arguments
def moment_y_reference(
    moment_y_p: float,
    force_x: float,
    force_z: float,
    x_coord_p: float,
    z_coord_p: float,
    x_coord_u: float = 0,
    z_coord_u: float = 0,
) -> float:
    r"""
    Calculate moment_y_reference

    :math:`M_{yU} = M_{yP} + F_{x}\cdot (z_{P} - z_{U}) - F_{z}\cdot (x_{P} - x_{U})`

    :param moment_y_p: moment of the force about the point of application in the y direction
    :type moment_y_p: float
    :param force_x: force in the x direction
    :type force_x: float
    :param force_z: force in the z direction
    :type force_z: float
    :param x_coord_p: x coordinate of the point of application of the force
    :type x_coord_p: float
    :param z_coord_p: z coordinate of the point of application of the force
    :type z_coord_p: float
    :param x_coord_u: x coordinate of the point of reference of the force
    :type x_coord_u: float
    :param z_coord_u: z coordinate of the point of reference of the force
    :type z_coord_u: float
    :return moment_myu: moment of the force about the point of reference in the y direction
    :rtype: float

    """

    moment_y_ref = (
        moment_y_p
        + force_x * (z_coord_p - z_coord_u)
        - force_z * (x_coord_p - x_coord_u)
    )
    return float(moment_y_ref)


# pylint: disable=too-many-arguments
def moment_y_reference_markdown(
    moment_y_p: float,
    force_x: float,
    force_z: float,
    x_coord_p: float,
    z_coord_p: float,
    x_coord_u: float = 0,
    z_coord_u: float = 0,
) -> tuple:
    """
    Create markdown in LaTeX for moment_y_reference
    NOTE: Changed slightly from the HSB to insert absolute coordinates for both applied and
    reference points

    :param moment_y_p: moment of the force about the point of application in the y direction
    :type moment_y_p: float
    :param force_x: force in the x direction
    :type force_x: float
    :param force_z: force in the z direction
    :type force_z: float
    :param x_coord_p: x coordinate of the point of application of the force
    :type x_coord_p: float
    :param z_coord_p: z coordinate of the point of application of the force
    :type z_coord_p: float
    :param x_coord_u: x coordinate of the point of reference of the force
    :type x_coord_u: float
    :param z_coord_u: z coordinate of the point of reference of the force
    :type z_coord_u: float
    :return markdown: markdown in LaTeX for moment_y_reference
    :rtype: str

    """

    moment_y_ref = moment_y_reference(
        moment_y_p, force_x, force_z, x_coord_p, z_coord_p, x_coord_u, z_coord_u
    )
    # for LaTeX
    # pylint: disable=anomalous-backslash-in-string
    markdown_formula = r"""$$
    M_{yU} = M_{yP} + F_{x}\cdot (z_{P} - z_{U}) - F_{z}\cdot (x_{P} - x_{U})
    $$

    """
    markdown_filled = (
        f"$${moment_y_ref} = "
        f"{moment_y_p} + {force_x} "
        r"\cdot "
        f"({z_coord_p} - {z_coord_u}) - "
        f"{force_z} "
        r"\cdot "
        f"({x_coord_p} - {x_coord_u})$$"
    )
    # pylint: enable=anomalous-backslash-in-string
    return markdown_formula, markdown_filled


# pylint: disable=too-many-arguments
def moment_z_reference(
    moment_z_p: float,
    force_x: float,
    force_y: float,
    x_coord_p: float,
    y_coord_p: float,
    x_coord_u: float = 0,
    y_coord_u: float = 0,
) -> float:
    r"""
    Calculates the moment of the force about the point of application in the z direction.

    :math: `M_{zU} = M_{zP} - F_{x}\cdot (y_{P} - y_{U}) + F_{y}\cdot (x_{P} - x_{U})`

    :param moment_z_p: moment of the force about the point of application in the z direction
    :type moment_z_p: float
    :param force_x: force in the x direction
    :type force_x: float
    :param force_y: force in the y direction
    :type force_y: float
    :param x_coord_p: x coordinate of the point of application of the force
    :type x_coord_p: float
    :param y_coord_p: y coordinate of the point of application of the force
    :type y_coord_p: float
    :param x_coord_u: x coordinate of the point of reference of the force
    :type x_coord_u: float
    :param y_coord_u: y coordinate of the point of reference of the force
    :type y_coord_u: float
    :return moment_mz: moment of the force about the point of reference in the z direction
    :rtype: float

    """

    moment_z_ref = (
        moment_z_p
        - force_x * (y_coord_p - y_coord_u)
        + force_y * (x_coord_p - x_coord_u)
    )

    return float(moment_z_ref)


def moment_z_reference_markdown(
    moment_z_p: float,
    force_x: float,
    force_y: float,
    x_coord_p: float,
    y_coord_p: float,
    x_coord_u: float = 0,
    y_coord_u: float = 0,
) -> tuple:
    r"""
    Create markdown in LaTeX for moment_z_reference
    NOTE: Changed slightly from the HSB to insert absolute coordinates for both applied and
    reference points

    :param moment_z_p: moment of the force about the point of application in the z direction
    :type moment_z_p: float
    :param force_x: force in the x direction
    :type force_x: float
    :param force_y: force in the y direction
    :type force_y: float
    :param x_coord_p: x coordinate of the point of application of the force
    :type x_coord_p: float
    :param y_coord_p: y coordinate of the point of application of the force
    :type y_coord_p: float
    :param x_coord_u: x coordinate of the point of reference of the force
    :type x_coord_u: float
    :param y_coord_u: y coordinate of the point of reference of the force
    :type y_coord_u: float
    :return markdown: markdown in LaTeX for moment_z_reference
    :rtype: str

    """

    moment_z_ref = moment_z_reference(
        moment_z_p, force_x, force_y, x_coord_p, y_coord_p, x_coord_u, y_coord_u
    )
    # for LaTeX
    # pylint: disable=anomalous-backslash-in-string
    markdown_formula = r"""$$
    M_{zU} = M_{zP} - F_{x}\cdot (y_{P} - y_{U}) + F_{y}\cdot (x_{P} - x_{U})
    $$

    """
    markdown_filled = (
        f"$${moment_z_ref} = "
        f"{moment_z_p} - {force_x} "
        r"\cdot"
        f" ({y_coord_p} - {y_coord_u}) + "
        f"{force_y} "
        r"\cdot"
        f" ({x_coord_p} - {x_coord_u})$$"
    )
    # pylint: enable=anomalous-backslash-in-string
    return markdown_formula, markdown_filled


def moments_transformation(
    moments: namedtuple, forces: namedtuple, application_point: namedtuple
) -> namedtuple:
    """
    Calculates the moments of the force about the point of application.

    :param moments: moments of the force about the point of application
    :type moments: namedtuple
    :param forces: forces in the x, y, z directions
    :type forces: namedtuple
    :param application_point: coordinates of the point of application of the force
    :type application_point: namedtuple
    :return moments_ref: moments of the force about the point of reference
    :rtype: namedtuple

    """

    moment_x_u = moment_x_reference(
        moments.moment_x,
        forces.force_y,
        forces.force_z,
        application_point.y_coord,
        application_point.z_coord,
    )

    moment_y_u = moment_y_reference(
        moments.moment_y,
        forces.force_x,
        forces.force_z,
        application_point.x_coord,
        application_point.z_coord,
    )

    moment_z_u = moment_z_reference(
        moments.moment_z,
        forces.force_x,
        forces.force_y,
        application_point.x_coord,
        application_point.y_coord,
    )

    moments_u = namedtuple(
        "moments_u",
        [
            "moment_x_u",
            "moment_y_u",
            "moment_z_u",
        ],
    )

    moments_u = moments_u(moment_x_u, moment_y_u, moment_z_u)

    return moments_u


# TODO: moments_transformation implemented with numpy array for speed and general use


# def AbsMaxND(a, axis=None):
#    """
#    Return the absolute maximum of an array along a given axis.
#    """
#    amax = a.max(axis)
#    amin = a.min(axis)
#    return np.where(-amin > amax, amin, amax)


def riv_field(
    forces, moments, application_point, rivets
):  # pylint: disable=too-many-locals
    """
    Rivet field calculation as given in HSB 21030-01

    Args:
        forces(float array): Applied forces for the rivet field (Fy,Fy,Fz)
        moments(float array): applied moments for the rivet field (Mx,My,Mz)
        application_point(float array): coordinates of the application point (X,Y,Z)
        rivets(pandas DataFrame): DataFrame with rivet definition (position) and allowables.
                                  Columns expected are (Shear,Tension,X,Y)

    Returns:
        res(DataFrame): Result Dataframe based on input DF and with appended result columns.
        CGs(DataFrame): CG information from rivet field, to be used in plotting function.

    """
    moment_mxu = (
        moments[0] - forces[1] * application_point[2] + forces[2] * application_point[1]
    )
    moment_myu = (
        moments[1] + forces[0] * application_point[2] - forces[2] * application_point[0]
    )
    moment_mzu = (
        moments[2] - forces[0] * application_point[1] + forces[1] * application_point[0]
    )

    cg_ys = sum(rivets.Shear * rivets.X) / sum(rivets.Shear)
    cg_zs = sum(rivets.Shear * rivets.Y) / sum(rivets.Shear)
    # Calculation for tension assuming same material of rivets. If different materials are used,
    # allowables should be scaled by ratio of young moduli
    cg_yt = sum(rivets.Tension * rivets.X) / sum(rivets.Tension)
    cg_zt = sum(rivets.Tension * rivets.Y) / sum(rivets.Tension)

    moment_mxs = moment_mxu + forces[1] * cg_zs - forces[2] * cg_ys
    moment_mys = moment_myu - forces[0] * cg_zt
    moment_mzs = moment_mzu + forces[0] * cg_yt

    alpha = (
        math.atan(
            2
            * sum(rivets.Tension * (rivets.X - cg_yt) * (rivets.Y - cg_zt))
            / (
                sum(rivets.Tension * (rivets.X - cg_yt) ** 2)
                - sum(rivets.Tension * (rivets.Y - cg_zt) ** 2)
            )
        )
        / 2
    )
    coord_yta = cg_yt * math.cos(alpha) + cg_zt * math.sin(alpha)
    coord_zta = -cg_yt * math.sin(alpha) + cg_zt * math.cos(alpha)
    coord_ya = rivets.X * math.cos(alpha) + rivets.Y * math.sin(alpha)
    coord_za = -rivets.X * math.sin(alpha) + rivets.Y * math.cos(alpha)
    moment_mysa = moment_mys * math.cos(alpha) + moment_mzs * math.sin(alpha)
    moment_mzsa = -moment_mys * math.sin(alpha) + moment_mzs * math.cos(alpha)

    force_fsy = forces[1] * rivets.Shear / sum(rivets.Shear) - moment_mxs * (
        rivets.Shear * (rivets.Y - cg_zs)
    ) / sum(rivets.Shear * ((rivets.X - cg_ys) ** 2 + (rivets.Y - cg_zs) ** 2))
    force_fsz = forces[2] * rivets.Shear / sum(rivets.Shear) + moment_mxs * (
        rivets.Shear * (rivets.X - cg_ys)
    ) / sum(rivets.Shear * ((rivets.X - cg_ys) ** 2 + (rivets.Y - cg_zs) ** 2))
    force_fs = np.sqrt(force_fsy**2 + force_fsz**2)

    force_f1 = forces[0] * rivets.Tension / sum(rivets.Tension)
    force_f2 = (
        moment_mysa
        * (rivets.Tension * (coord_za - coord_zta))
        / sum(rivets.Tension * (coord_za - coord_zta) ** 2)
    )
    force_f3 = (
        moment_mzsa
        * (rivets.Tension * (coord_ya - coord_yta))
        / sum(rivets.Tension * (coord_ya - coord_yta) ** 2)
    )
    force_ft = force_f1 + force_f2 - force_f3
    shear_reserve_factor = np.trunc(100 * rivets.Shear / force_fs) / 100
    tension_reserve_factor = np.trunc(100 * rivets.Tension / force_ft) / 100
    # expanding the rivet input DF with results
    res = rivets.copy()
    res.insert(4, "Fsy", force_fsy)
    res.insert(5, "Fsz", force_fsz)
    res.insert(6, "Fs", force_fs)
    res.insert(7, "Ft", force_ft)
    res.insert(8, "RFs", shear_reserve_factor)
    res.insert(9, "RFt", tension_reserve_factor)
    res = res.astype({"Fsy": "int64", "Fsz": "int64", "Fs": "int64", "Ft": "int64"})
    # creating a matrix with the CG information for further use in other functions
    centers_of_gravity = [
        application_point[1],
        application_point[2],
        cg_ys,
        cg_zs,
        cg_yt,
        cg_zt,
    ]
    return res, centers_of_gravity
