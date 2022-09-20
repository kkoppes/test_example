"""module for HSB method 21030-01"""

from array import array
from collections import namedtuple
from dataclasses import dataclass, field
import math
from typing import List
import numpy as np
import pandas as pd

def moment_x_reference(
    moment_x_p: float,
    force_y: float,
    force_z: float,
    z_coord_p: float,
    y_coord_p: float,
    z_coord_u: float = 0,
    y_coord_u: float = 0,
) -> float:
    """
    Calculates the moment of the force about the point of application in the x direction.
    NOTE: Changed slightly from the HSB to insert absolute coordinates for both applied and reference points
    args:
        m_moment_x_px_p(float): moment of the force
                                about the point of application in the x direction
        force_y(float): force in the y direction
        force_z(float): force in the z direction
        z_coord_p(float): z coordinate of the point of application of the force
        y_coord_p(float): y coordinate of the point of application of the force
        y_coord_u(float): y coordinate of the point of reference of the force
    returns:
        moment_mxu(float): moment of the force about the point of application in the x direction
    """

    moment_x_ref = (
        moment_x_p
        - force_y * (z_coord_p - z_coord_u)
        + force_z * (y_coord_p - y_coord_u)
    )
    return float(moment_x_ref)


# markdown of this function above
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
    NOTE: Changed slightly from the HSB to insert absolute coordinates for both applied and reference points
    args:
        moment_x_p(float): moment of the force
                                about the point of application in the x direction
        force_y(float): force in the y direction
        force_z(float): force in the z direction
        z_coord_p(float): z coordinate of the point of application of the force
        y_coord_p(float): y coordinate of the point of application of the force
        y_coord_u(float): y coordinate of the point of reference of the force
    returns:
        markdown(str): markdown in LaTeX for moment_x_reference
    """

    moment_x_ref = moment_x_reference(
        moment_x_p, force_y, force_z, z_coord_p, y_coord_p, z_coord_u, y_coord_u
    )
    # for LaTeX
    # pylint: disable=anomalous-backslash-in-string
    markdown_formula = """$$
    M_{xU} = M_{xP} - F_{y}\cdot (z_{P} - z_{U}) + F_{z}\cdot (y_{P} - y_{U})
    $$

    """
    markdown_filled = (
        f"$${moment_x_ref} = "
        f"{moment_x_p} - {force_y} \cdot ({z_coord_p} - {z_coord_u}) + {force_z} \cdot ({y_coord_p} - {y_coord_u})$$"
    )
    # pylint: enable=anomalous-backslash-in-string
    return (markdown_formula, markdown_filled)



def moment_y_reference(
    moment_y_p: float,
    force_x: float,
    force_z: float,
    x_coord_p: float,
    z_coord_p: float,
    x_coord_u: float = 0,
    z_coord_u: float = 0,
) -> float:
    """
    Calculate moment_y_reference
    args:
        moment_y_p(float): moment of the force
                                about the point of application in the y direction
        force_x(float): force in the x direction
        force_z(float): force in the z direction
        x_coord_p(float): x coordinate of the point of application of the force
        z_coord_p(float): z coordinate of the point of application of the force
        x_coord_u(float): x coordinate of the point of reference of the force
        z_coord_u(float): z coordinate of the point of reference of the force
    returns:
        moment_myu(float): moment of the force about the point of application in the y direction
    """

    moment_y_ref = (
        moment_y_p
        + force_x * (z_coord_p - z_coord_u)
        - force_z * (x_coord_p - x_coord_u)
    )
    return float(moment_y_ref)


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
    NOTE: Changed slightly from the HSB to insert absolute coordinates for both applied and reference points
    args:
        moment_y_p(float): moment of the force
                                about the point of application in the y direction
        force_x(float): force in the x direction
        force_z(float): force in the z direction
        x_coord_p(float): x coordinate of the point of application of the force
        z_coord_p(float): z coordinate of the point of application of the force
        x_coord_u(float): x coordinate of the point of reference of the force
        z_coord_u(float): z coordinate of the point of reference of the force
    returns:
        markdown(str): markdown in LaTeX for moment_y_reference
    """

    moment_y_ref = moment_y_reference(
        moment_y_p, force_x, force_z, x_coord_p, z_coord_p, x_coord_u, z_coord_u
    )
    # for LaTeX
    # pylint: disable=anomalous-backslash-in-string
    markdown_formula = """$$
    M_{yU} = M_{yP} + F_{x}\cdot (z_{P} - z_{U}) - F_{z}\cdot (x_{P} - x_{U})
    $$

    """
    markdown_filled = (
        f"$${moment_y_ref} = "
        f"{moment_y_p} + {force_x} \cdot ({z_coord_p} - {z_coord_u}) - {force_z} \cdot ({x_coord_p} - {x_coord_u})$$"
    )
    # pylint: enable=anomalous-backslash-in-string
    return markdown_formula, markdown_filled



def moment_z_reference(
    moment_z_p: float,
    force_x: float,
    force_y: float,
    x_coord_p: float,
    y_coord_p: float,
    x_coord_u: float = 0,
    y_coord_u: float = 0,
) -> float:
    """
    Calculates the moment of the force about the point of application in the z direction.
    args:
        moment_z_p(float): moment of the force
                                about the point of application in the z direction
        force_x(float): force in the x direction
        force_y(float): force in the y direction
        x_coord_p(float): x coordinate of the point of application of the force
        y_coord_p(float): y coordinate of the point of application of the force
        x_coord_u(float): x coordinate of the point of reference of the force
        y_coord_u(float): y coordinate of the point of reference of the force
    returns:
        moment_z_ref(float): moment of the force about the point of application in the z direction
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
    """
    Create markdown in LaTeX for moment_z_reference
    NOTE: Changed slightly from the HSB to insert absolute coordinates for both applied and reference points
    args:
        moment_z_p(float): moment of the force
                                about the point of application in the z direction
        force_x(float): force in the x direction
        force_y(float): force in the y direction
        x_coord_p(float): x coordinate of the point of application of the force
        y_coord_p(float): y coordinate of the point of application of the force
        x_coord_u(float): x coordinate of the point of reference of the force
        y_coord_u(float): y coordinate of the point of reference of the force
    returns:
        markdown(str): markdown in LaTeX for moment_z_reference
    """

    moment_z_ref = moment_z_reference(
        moment_z_p, force_x, force_y, x_coord_p, y_coord_p, x_coord_u, y_coord_u
    )
    # for LaTeX
    # pylint: disable=anomalous-backslash-in-string
    markdown_formula = """$$
    M_{zU} = M_{zP} - F_{x}\cdot (y_{P} - y_{U}) + F_{y}\cdot (x_{P} - x_{U})
    $$

    """
    markdown_filled = (
        f"$${moment_z_ref} = "
        f"{moment_z_p} - {force_x} \cdot ({y_coord_p} - {y_coord_u}) + {force_y} \cdot ({x_coord_p} - {x_coord_u})$$"
    )
    # pylint: enable=anomalous-backslash-in-string
    return markdown_formula, markdown_filled

def moments_transformation(
    moments: namedtuple, forces: namedtuple, application_point: namedtuple
) -> namedtuple:
    """
    Calculates the moments of the force about the point of application.
    args:
        moments(namedtuple): moments of the force about the point of application
        forces(namedtuple): forces in the x, y, and z directions
        application_point(namedtuple): point of application of the force
        TODO: add reference_point(namedtuple): reference point
    returns:
        moments_u(namedtuple): moments of the force about the point of application
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


@dataclass
class ReferencePoint:
    """
    Class for moment/load reference points
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


@dataclass
class Forces:
    """
    Class for forces
    """

    name: str
    force_x: float
    force_y: float
    force_z: float
    namedtuple: namedtuple = None

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


@dataclass
class Moments:
    """
    Class for moments
    """

    name: str
    moment_x: float
    moment_y: float
    moment_z: float
    namedtuple: namedtuple = None

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


@dataclass
class Fastener:
    """
    Class for fastener
    """

    name: str
    specification: str
    shear_allowable: float
    tension_allowable: float
    x_coord: float
    y_coord: float
    z_coord: float

    # optional material
    material: str = "mymaterial"

    # TODO: add material to fastener (from material database)


@dataclass
class FastenerGroup:
    """
    Class for fastener group
    """

    name: str
    fasteners: list
    X: array = field(init=False)
    Y: array = field(init=False)
    # TODO: add Z?
    shear: array = field(init=False)
    tension: array = field(init=False)
    # centroid: default = None
    centroid_ys: namedtuple = field(init=False)
    centroid_zs: namedtuple = field(init=False)
    centroid_yt: namedtuple = field(init=False)
    centroid_zt: namedtuple = field(init=False)

    dataframe: pd.DataFrame = field(init=False)

    def __post_init__(self):
        """
        Post initialization of fastener group
        """
        # default name
        if self.name == "":
            self.name = "FastenerGroup"

        # X array from fasteners
        self.X = np.array([fastener.x_coord for fastener in self.fasteners])
        # Y array from fasteners
        self.Y = np.array([fastener.y_coord for fastener in self.fasteners])
        # shear array from fasteners
        self.shear = np.array([fastener.shear_allowable for fastener in self.fasteners])
        # tension array from fasteners
        self.tension = np.array(
            [fastener.tension_allowable for fastener in self.fasteners]
        )

        # centroid_ys = sum(fastener.Shear * fastener.X) / sum(fastener.Shear)
        # centroid_zs = sum(fastener.Shear * fastener.Y) / sum(fastener.Shear)
        self.centroid_ys = self.calculate_centroid_ys()
        self.centroid_zs = self.calculate_centroid_zs()

        # Calculation for tension assuming same material of rivets. If different materials are used,
        # centroid_yt = sum(fastener.Tension * fastener.X) / sum(fastener.Tension)
        # centroid_zt = sum(fastener.Tension * fastener.Y) / sum(fastener.Tension)
        # allowables should be scaled by ratio of young moduli
        self.centroid_yt = self.calculate_centroid_yt()
        self.centroid_zt = self.calculate_centroid_zt()

        # dataframe
        self.dataframe = self.create_dataframe()

    def calculate_centroid_ys(self) -> namedtuple:
        """
        Calculates centroid of fastener group in y direction
        """
        centroid_ys = sum(
            [fastener.y_coord * fastener.shear_allowable for fastener in self.fasteners]
        ) / sum([fastener.shear_allowable for fastener in self.fasteners])
        return centroid_ys

    def calculate_centroid_zs(self) -> namedtuple:
        """
        Calculates centroid of fastener group in z direction
        """
        centroid_zs = sum(
            [fastener.z_coord * fastener.shear_allowable for fastener in self.fasteners]
        ) / sum([fastener.shear_allowable for fastener in self.fasteners])
        return centroid_zs

    def calculate_centroid_yt(self) -> namedtuple:
        """
        Calculates centroid of fastener group in y direction, TODO: scaled by E
        """
        centroid_yt = sum(
            [
                fastener.y_coord * fastener.tension_allowable
                for fastener in self.fasteners
            ]
        ) / sum([fastener.tension_allowable for fastener in self.fasteners])
        return centroid_yt

    def calculate_centroid_zt(self) -> namedtuple:
        """
        Calculates centroid of fastener group in z direction, TODO: scaled by E
        """
        centroid_zt = sum(
            [
                fastener.z_coord * fastener.tension_allowable
                for fastener in self.fasteners
            ]
        ) / sum([fastener.tension_allowable for fastener in self.fasteners])
        return centroid_zt

    # add fastener to fastener group
    def add_fastener(self, fastener) -> None:
        """
        Adds fastener to fastener group
        """
        self.fasteners.append(fastener)
        # calculate new centroid
        self.centroid_ys = self.calculate_centroid_ys()
        self.centroid_zs = self.calculate_centroid_zs()
        self.centroid_yt = self.calculate_centroid_yt()
        self.centroid_zt = self.calculate_centroid_zt()

    def update_fastener(self, fastener, attribute, value) -> None:
        """
        Updates fastener in fastener group
        """
        # update fastener
        fastener.__setattr__(attribute, value)
        # calculate new centroid
        self.centroid_ys = self.calculate_centroid_ys()
        self.centroid_zs = self.calculate_centroid_zs()
        self.centroid_yt = self.calculate_centroid_yt()
        self.centroid_zt = self.calculate_centroid_zt()
        self.dataframe = self.create_dataframe()

    def create_dataframe(self) -> pd.DataFrame:
        """
        Creates dataframe for fastener group
        """
        dataframe = pd.DataFrame(
            {
                "name": [fastener.name for fastener in self.fasteners],
                "specification": [
                    fastener.specification for fastener in self.fasteners
                ],
                "X": [fastener.x_coord for fastener in self.fasteners],
                "Y": [fastener.y_coord for fastener in self.fasteners],
                "Z": [fastener.z_coord for fastener in self.fasteners],
                "Shear": [fastener.shear_allowable for fastener in self.fasteners],
                "Tension": [fastener.tension_allowable for fastener in self.fasteners],
            }
        )

        # add optional columns
        # material: str = None

        if self.fasteners[0].material is not None:
            dataframe["Material"] = [fastener.material for fastener in self.fasteners]

        return dataframe


class HSB_21030_01:
    """
    Class for HSB 21030-01 fastener calculation
    """

    def __init__(
        self,
        id: str,
        fastener_group: FastenerGroup,
        forces: namedtuple,
        moments: namedtuple,
        application_point: namedtuple,
        reference_point: namedtuple,
    ):
        """
        Initialization of HSB 21030-01 fastener calculation
        """
        self.id = id
        self.fastener_group = fastener_group
        self.forces = forces
        self.moments = moments
        self.application_point = application_point
        self.reference_point = (
            reference_point  # namedtuple("reference_point", ["x", "y", "z"])(0, 0, 0)
        )
        # moment around reference point
        self.moments_u = moments_transformation(
            self.moments, self.forces, self.application_point
        )

        # calculate moment around centroid
        # TODO: make moments_s namedtuple
        # moment_mxs = moment_mxu + forces[1] * cg_zs - forces[2] * cg_ys
        self.moment_x_s = moment_x_reference(
            moment_x_p=self.moments_u.moment_x_u,
            force_y=self.forces.force_y,
            force_z=self.forces.force_z,
            z_coord_p=self.reference_point.z_coord,
            y_coord_p=self.reference_point.y_coord,
            z_coord_u=self.fastener_group.centroid_zs,
            y_coord_u=self.fastener_group.centroid_ys,
        )

        # moment_mys = moment_myu - forces[0] * cg_zt
        self.moment_y_s = moment_y_reference(
            moment_y_p=self.moments_u.moment_y_u,
            force_x=self.forces.force_x,
            force_z=0,
            x_coord_p=0,
            z_coord_p=0,
            x_coord_u=0,
            z_coord_u=self.fastener_group.centroid_zt,
        )
        # moment_mzs = moment_mzu + forces[0] * cg_yt
        self.moment_z_s = moment_z_reference(
            moment_z_p=self.moments_u.moment_z_u,
            force_x=self.forces.force_x,
            force_y=0,
            x_coord_p=0,
            y_coord_p=0,
            x_coord_u=0,
            y_coord_u=self.fastener_group.centroid_yt,
        )

        # calculate alpha
        self.alpha = self.calculate_alpha()

        # calculation of transformed coordinates:
        self.centroid_yta = self.calculate_centroid_yta()
        self.centroid_zta = self.calculate_centroid_zta()

        self.fastener_ya = self.calculate_fastener_ya()
        self.fastener_za = self.calculate_fastener_za()

        # calculation of transformed moments:
        self.moment_ya = self.calculate_moment_ya()
        self.moment_za = self.calculate_moment_za()

        # calculation of transformed forces:
        self.force_fsy = self.calculate_fsy()
        self.force_fsz = self.calculate_fsz()
        self.shear_forces = self.calculate_fastener_shear_forces()

        # tension force
        self.force_f1 = self.calculate_fastener_tension_force_f1()
        self.force_f2 = self.calculate_fastener_tension_force_f2()
        self.force_f3 = self.calculate_fastener_tension_force_f3()
        self.tension_forces = self.calculate_fastener_tension_force()

        # reserve factor calculation
        self.reserve_factor_shear = self.calculate_fastener_shear_reserve_factor()
        self.reserve_factor_tension = self.calculate_fastener_tension_reserve_factor()

        # check if fastener is in tension or compression
        self.fastener_tension = self.check_fastener_tension()

        self.dataframe = self.make_dataframe()

        self.cogs = self.make_cogs()

        #update fastener group with 0 tension allowable for fasteners under compression
        #self.fastener_group.update_fasteners_tension_allowable(self.fastener_tension)


    def calculate_alpha(self) -> float:
        """
        Calculates the angle alpha
        """
        alpha = (
            math.atan(
                2
                * sum(
                    [
                        fastener.tension_allowable
                        * (fastener.y_coord - self.fastener_group.centroid_yt)
                        * (fastener.z_coord - self.fastener_group.centroid_zt)
                        for fastener in self.fastener_group.fasteners
                    ]
                )
                / (
                    sum(
                        [
                            fastener.tension_allowable
                            * (fastener.y_coord - self.fastener_group.centroid_yt) ** 2
                            for fastener in self.fastener_group.fasteners
                        ]
                    )
                    - sum(
                        [
                            fastener.tension_allowable
                            * (fastener.z_coord - self.fastener_group.centroid_zt) ** 2
                            for fastener in self.fastener_group.fasteners
                        ]
                    )
                )
            )
            / 2
        )
        return alpha

    def calculate_centroid_yta(self) -> float:
        """
        Calculates the transformed y-coordinate of the centroid
        """
        return self.fastener_group.centroid_yt * math.cos(
            self.alpha
        ) + self.fastener_group.centroid_zt * math.sin(self.alpha)

    def calculate_centroid_zta(self) -> float:
        """
        Calculates the transformed z-coordinate of the centroid
        """
        return -self.fastener_group.centroid_yt * math.sin(
            self.alpha
        ) + self.fastener_group.centroid_zt * math.cos(self.alpha)

    def calculate_fastener_ya(self) -> List[float]:
        """
        Calculates the transformed y-coordinate of the fasteners
        """
        return [
            fastener.y_coord * math.cos(self.alpha)
            + fastener.z_coord * math.sin(self.alpha)
            for fastener in self.fastener_group.fasteners
        ]

    def calculate_fastener_za(self) -> List[float]:
        """
        Calculates the transformed z-coordinate of the fasteners
        """
        return [
            -fastener.y_coord * math.sin(self.alpha)
            + fastener.z_coord * math.cos(self.alpha)
            for fastener in self.fastener_group.fasteners
        ]

    def calculate_moment_ya(self) -> List[float]:
        """
        Calculates the transformed moments in y-direction
        """
        return self.moment_y_s * math.cos(self.alpha) + self.moment_z_s * math.sin(
            self.alpha
        )

    def calculate_moment_za(self) -> List[float]:
        """
        Calculates the transformed moments in z-direction
        """
        return -self.moment_y_s * math.sin(self.alpha) + self.moment_z_s * math.cos(
            self.alpha
        )

    def calculate_fastener_tension_force_f1(self) -> float:
        force_f1 = (
            self.forces.force_x
            * self.fastener_group.tension
            / sum(self.fastener_group.tension)
        )
        return force_f1

    def calculate_fastener_tension_force_f2(self) -> List[float]:
        za = pd.Series(self.fastener_za)
        force_f2 = (
            self.moment_ya
            * (self.fastener_group.tension * (za - self.centroid_zta))
            / sum(self.fastener_group.tension * (za - self.centroid_zta) ** 2)
        )
        return force_f2

    def calculate_fastener_tension_force_f3(self) -> List[float]:
        ya = pd.Series(self.fastener_ya)
        force_f3 = (
            self.moment_za
            * (self.fastener_group.tension * (ya - self.centroid_yta))
            / sum(self.fastener_group.tension * (ya - self.centroid_yta) ** 2)
        )
        return force_f3

    def calculate_fastener_tension_force(self) -> List[float]:
        force_ft = self.force_f1 + self.force_f2 - self.force_f3
        return force_ft

    def calculate_fsz(self) -> float:
        force_fsz = self.forces.force_z * self.fastener_group.shear / sum(
            self.fastener_group.shear
        ) + self.moment_x_s * (
            self.fastener_group.shear
            * [
                (fastener.y_coord - self.fastener_group.centroid_ys)
                for fastener in self.fastener_group.fasteners
            ]
        ) / sum(
            self.fastener_group.shear
            * (
                np.array(
                    [
                        (fastener.y_coord - self.fastener_group.centroid_ys) ** 2
                        for fastener in self.fastener_group.fasteners
                    ]
                )
                + np.array(
                    [
                        (fastener.z_coord - self.fastener_group.centroid_zs) ** 2
                        for fastener in self.fastener_group.fasteners
                    ]
                )
            )
        )
        return force_fsz

    def calculate_fsy(self) -> float:

        force_fsy = self.forces.force_y * self.fastener_group.shear / sum(
            self.fastener_group.shear
        ) - self.moment_x_s * (
            self.fastener_group.shear
            * [
                (fastener.z_coord - self.fastener_group.centroid_zs)
                for fastener in self.fastener_group.fasteners
            ]
        ) / sum(
            self.fastener_group.shear
            * (
                np.array(
                    [
                        (fastener.y_coord - self.fastener_group.centroid_ys) ** 2
                        for fastener in self.fastener_group.fasteners
                    ]
                )
                + np.array(
                    [
                        (fastener.z_coord - self.fastener_group.centroid_zs) ** 2
                        for fastener in self.fastener_group.fasteners
                    ]
                )
            )
        )
        return force_fsy

    def calculate_fastener_shear_forces(self) -> List[float]:
        # force_fsy = self.calculate_fsy()

        # force_fsz = self.calculate_fsz()

        force_fs = np.sqrt(self.force_fsy**2 + self.force_fsz**2)

        return force_fs

    # shear_reserve_factor = np.trunc(100 * rivets.Shear / force_fs) / 100
    def calculate_fastener_shear_reserve_factor(self) -> float:
        return np.trunc(100 * self.fastener_group.shear / self.shear_forces) / 100

    # tension_reserve_factor = np.trunc(100 * rivets.Tension / force_ft) / 100
    def calculate_fastener_tension_reserve_factor(self) -> float:
        return np.trunc(100 * self.fastener_group.tension / self.tension_forces) / 100

    def make_dataframe(self):
        """make dataframe including fasteners, attributes, forces and reserve factors"""
        df = {
            "X": self.fastener_group.X,
            "Y": self.fastener_group.Y,
            "Shear": self.fastener_group.shear,
            "Tension": self.fastener_group.tension,
            "Fsyi": self.force_fsy,
            "Fsz": self.force_fsz,
            "Shear Force": self.shear_forces,
            "Tension Force": self.tension_forces,
            "Shear Reserve Factor": self.reserve_factor_shear,
            "Tension Reserve Factor": self.reserve_factor_tension,
        }
        return df

    def check_fastener_tension(self):
        for i, t_force in enumerate(self.tension_forces):
            if i < 0:
                print(f"fastener {i} is in compression: {t_force}")
            else:
                print(f"fastener {i} is in tension: {t_force}")

    def make_cogs(self):
        """make dataframe including fasteners, attributes, forces and reserve factors"""
        df = {
            "application_point_x": self.application_point.x_coord,
            "application_point_y": self.application_point.y_coord,
            "application_point_z": self.application_point.z_coord,
            "centroid_ys": self.fastener_group.centroid_ys,
            "centroid_zs": self.fastener_group.centroid_zs,
            "centroid_yt": self.fastener_group.centroid_yt,
            "centroid_zt": self.fastener_group.centroid_zt
        }
        return df

def riv_field(forces, moments, application_point, rivets):
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
