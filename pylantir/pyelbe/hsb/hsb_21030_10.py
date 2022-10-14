"""module for HSB method 21030-01"""


from collections import namedtuple

from dataclasses import dataclass, field
import math
from typing import List
import numpy as np
import pandas as pd

from pylantir.pyweser.matreel.material import Material
from pylantir.pyelbe.loads import Forces, Moments
from pylantir.pyelbe.abstractions import ReferencePoint
from pylantir.pyelbe.fasteners import Fastener, FastenerGroup
from .hsb_formulas import (
    moment_x_reference,
    moment_y_reference,
    moment_z_reference,
    moments_transformation,
)

class Hsb2103001:  # pylint: disable=too-many-public-methods
    """
    Internal load distribution of fastener groups 21030-01 Issue D Year 1989

    Summary
    This sheet provides a method to calculate the shear and tensile forces in fastener groups.
    Key Words: Fastener group, shear force, tension force

    This sheet provides a method to calculate the shear and tensile forces for each fastener in
    riveted or bolted joints. The method is valid only for components that are sufficiently stiff in
    the joint area.
    For the static strength analyses the centroid of the fastener group is determined taking into
    account the allowable forces of the fasteners. For fatigue analyses the stiffnesses of the
    fasteners should be taken into account.

    Class for HSB 21030-01 fastener calculation
    """

    # TODO: add iteration trigger variable to take out dummy fastener from results
    def __init__(  # pylint: disable=too-many-arguments
        self,
        name: str,
        fastener_group: FastenerGroup,
        forces: namedtuple,
        moments: namedtuple,
        application_point: namedtuple,
        reference_point: namedtuple,
    ):
        """
        Initialization of HSB 21030-01 fastener calculation

        """
        self.name = name
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
        # application point 2D yz plane
        # reference point 2D yz plane
        # moment translation on plane to centroid for tension

        self.moment_x_s = self.calculate_mxs()

        self.moment_y_s = self.calculate_mys()

        self.moment_z_s = self.calculate_mzs()

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

        # if any fasteners are in compression, recalcultate with fastener tension allowable 0
        # update fastener tension allowable
        if [item for item in self.fastener_tension if not item[1]]:
            self.compression_update = True
            print("Fasteners in compression, iterate calculation!")

        self.result_dict = self.make_dict()

        self.cogs = self.make_cogs()

        # update fastener group with 0 tension allowable for fasteners under compression
        # self.fastener_group.update_fasteners_tension_allowable(self.fastener_tension)

    def calculate_mxs(self):
        r"""
        Calculate moment around centroid

        :math: `M_{xS} = M_{xU} + F_{y} \cdot z_{s} - F_{z} \cdot y_{s}`
        """
        # moment translation on plane to centroid for tension
        moment_x_s = moment_x_reference(
            moment_x_p=self.moments_u.moment_x_u,
            force_y=self.forces.force_y,
            force_z=self.forces.force_z,
            z_coord_p=self.reference_point.z_coord,
            y_coord_p=self.reference_point.y_coord,
            z_coord_u=self.fastener_group.centroid_zs,
            y_coord_u=self.fastener_group.centroid_ys,
        )
        return moment_x_s

    def calculate_mys(self):
        r"""

        :math: `M_{yS} = M_{yU} - F_{x} \cdot z_{T}`
        """
        moment_m_y_s = moment_y_reference(
            moment_y_p=self.moments_u.moment_y_u,
            force_x=self.forces.force_x,
            force_z=0,
            x_coord_p=0,
            z_coord_p=0,
            x_coord_u=0,
            z_coord_u=self.fastener_group.centroid_zt,
        )
        return moment_m_y_s

    def calculate_mzs(self):
        r"""

        :math: `M_{zS} = M_{zU} + F_{x} \cdot y_{T}`
        """
        moment_m_z_s = moment_z_reference(
            moment_z_p=self.moments_u.moment_z_u,
            force_x=self.forces.force_x,
            force_y=0,
            x_coord_p=0,
            y_coord_p=0,
            x_coord_u=0,
            y_coord_u=self.fastener_group.centroid_yt,
        )
        return moment_m_z_s

    def calculate_alpha(self) -> float:
        r"""
        Calculates the angle alpha
        3.3.3 Tensile forces in the fasteners
        To balance the forces it is necessary to transform the applied loading into the principal
        axis system of the fastener group.

        :math:`tan(2 \cdot \alpha) = 2 \cdot \frac{\sum[F_{T,all,i} \cdot (y_{i} -
         y_{T}) \cdot (z_{i} - z_{T})]}
        {\sum[F_{T,all,i} \cdot (y_{i} - y_{T})^{2}] - \sum[F_{T,all,i} \cdot (z_{i} - z_{T})^{2}]}`

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
        r"""
        Calculates the transformed y-coordinate of the centroid

        :math:`y_{T,a} = y_{T} * cos(\alpha) - z_{T} * sin(\alpha)`
        """
        return self.fastener_group.centroid_yt * math.cos(
            self.alpha
        ) + self.fastener_group.centroid_zt * math.sin(self.alpha)

    def calculate_centroid_zta(self) -> float:
        r"""
        Calculates the transformed z-coordinate of the centroid

        :math:`z_{T,a} =  - y_{T} * sin(\alpha) + z_{T} * cos(\alpha)`
        """
        return -self.fastener_group.centroid_yt * math.sin(
            self.alpha
        ) + self.fastener_group.centroid_zt * math.cos(self.alpha)

    def calculate_fastener_ya(self) -> List[float]:
        r"""
        Calculates the transformed y-coordinate of the fasteners

        :math:`y_{a,i} = y_{i} * cos(\alpha) - z_{i} * sin(\alpha)`
        """
        return [
            fastener.y_coord * math.cos(self.alpha)
            + fastener.z_coord * math.sin(self.alpha)
            for fastener in self.fastener_group.fasteners
        ]

    def calculate_fastener_za(self) -> List[float]:
        r"""
        Calculates the transformed z-coordinate of the fasteners

        :math:`z_{a,i} =  - y_{i} * sin(\alpha) + z_{i} * cos(\alpha)`
        """
        return [
            -fastener.y_coord * math.sin(self.alpha)
            + fastener.z_coord * math.cos(self.alpha)
            for fastener in self.fastener_group.fasteners
        ]

    def calculate_moment_ya(self) -> List[float]:
        r"""
        Calculates the transformed moments in y-direction

        :math:`M_{ySA} = M_{yS} * cos(\alpha) - M_{zS} * sin(\alpha)`
        """
        return self.moment_y_s * math.cos(self.alpha) + self.moment_z_s * math.sin(
            self.alpha
        )

    def calculate_moment_za(self) -> List[float]:
        r"""
        Calculates the transformed moments in z-direction

        :math:`M_{zSA} =  - M_{yS} * sin(\alpha) + M_{zS} * cos(\alpha)`
        """
        return -self.moment_y_s * math.sin(self.alpha) + self.moment_z_s * math.cos(
            self.alpha
        )

    def calculate_fastener_tension_force_f1(self) -> float:
        r"""
        3.3.3 Tensile forces in the fasteners
        To balance the forces it is necessary to transform the applied loading into the principal
        axis system of the fastener group

        :math:`F_{1,i} = F_{x}\cdot \frac{F_{t,all,i}}{\sum F_{t,all,i}}`
        """

        force_f1 = (
            self.forces.force_x
            * self.fastener_group.tension
            / sum(self.fastener_group.tension)
        )
        return force_f1

    def calculate_fastener_tension_force_f2(self) -> List[float]:
        r"""
        :math:`F_{2,i} = M_{ySA}\cdot \frac{\left [ F_{T,all,i} \cdot
                \left ( z_{Ai} - z_{TA} \right ) \right ]}{\sum \left [ F_{T,all,i} \cdot
                \left ( z_{Ai} - z_{TA} \right )^2 \right ]}`
        """
        za = pd.Series(self.fastener_za)  # pylint: disable=invalid-name
        force_f2 = (
            self.moment_ya
            * (self.fastener_group.tension * (za - self.centroid_zta))
            / sum(self.fastener_group.tension * (za - self.centroid_zta) ** 2)
        )
        return force_f2

    def calculate_fastener_tension_force_f3(self) -> List[float]:
        r"""
        :math:`F_{2,i} = M_{zSA}\cdot \frac{\left [ F_{T,all,i} \cdot
                \left ( y_{Ai} - y_{TA} \right ) \right ]}{\sum \left [ F_{T,all,i} \cdot
                \left ( y_{Ai} - y_{TA} \right )^2 \right ]}`
        """
        ya = pd.Series(self.fastener_ya)  # pylint: disable=invalid-name
        force_f3 = (
            self.moment_za
            * (self.fastener_group.tension * (ya - self.centroid_yta))
            / sum(self.fastener_group.tension * (ya - self.centroid_yta) ** 2)
        )
        return force_f3

    def calculate_fastener_tension_force(self) -> List[float]:
        """
        3.3.3 Tensile forces in the fasteners
        To balance the forces it is necessary to transform the applied loading into the principal
        axis system of the fastener group

        :math:`F_{i} = F_{1,i} + F_{2,i} + F_{3,i}`

        :param self.force_f1: force 1
        :param self.force_f2: force 2
        :param self.force_f3: force 3
        :return: tension forces
        """
        force_ft = self.force_f1 + self.force_f2 - self.force_f3
        return force_ft

    def calculate_fsz(self) -> float:
        r"""
        :math: `F_{S,z,i} = F_{z} - \frac{F_{S,all,i}}{\sum F_{S,all,i}} +
        M_{x,S} \cdot \frac{F_{S,all,i} \cdot (y_{i} - y_{s})}{\sum \left
        \{ F_{S,all,i} \cdot [(y_{i} - y_{S} )^{2} + (z_{i} - z_{s})^{2}] \right \}}`
        """
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
        r"""
        :math: `F_{S,y,i} = F_{y} + \frac {F_{S,all,i}}{\sum F_{S,all,i}} -
        M_{xS} \cdot \frac{F_{S,all,i} \cdot (z_{i} - z_{s})}{\sum \left
        \{ F_{S,all,i} \cdot [(y_{i} - y_{S} )^{2} + (z_{i} - z_{s})^{2}] \right \}}`
        """

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
        r"""
        3.3.4 Shear forces in the fasteners

        :math:`F_{S,i} = \sqrt{F_{S,z,i}^{2} + F_{S,y,i}^{2}}`



        :param self.force_fsz: force in z-direction
        :param self.force_fsy: force in y-direction
        :return: shear forces
        """

        force_fs = np.sqrt(self.force_fsy**2 + self.force_fsz**2)

        return force_fs

    def calculate_fastener_shear_reserve_factor(self) -> float:
        r"""
        :math: `RF = F_{s,all,i}/F_{s,i}`
        """
        return np.trunc(100 * self.fastener_group.shear / self.shear_forces) / 100

    def calculate_fastener_tension_reserve_factor(self) -> float:
        r"""
        :math: `RF = F_{t,all,i}/F_{t,i}`
        """
        return np.trunc(100 * self.fastener_group.tension / self.tension_forces) / 100

    def make_dict(self):
        """make dataframe including fasteners, attributes, forces and reserve factors"""
        df_dict = {
            "X": self.fastener_group.x_array,
            "Y": self.fastener_group.y_array,
            "Shear": self.fastener_group.shear,
            "Tension": self.fastener_group.tension,
            "Fsyi": self.force_fsy,
            "Fsz": self.force_fsz,
            "Shear Force": self.shear_forces,
            "Tension Force": self.tension_forces,
            "Shear Reserve Factor": self.reserve_factor_shear,
            "Tension Reserve Factor": self.reserve_factor_tension,
        }

        return df_dict

    def check_fastener_tension(self):
        """
        3.4 Additional forces due to the contact of the joined parts (compression)

        check if fasteners are in tension


        """
        tension = []
        for i, t_force in enumerate(self.tension_forces):
            if t_force < 0:
                # TODO: log warning with compression workaround
                print(
                    f"fastener {self.fastener_group.fastener_names[i]} is in compression: {t_force}"
                )
                tension.append((i, False))
            else:
                print(
                    f"fastener {self.fastener_group.fastener_names[i]} is in tension: {t_force}"
                )
                tension.append((i, True))
        return tension

    def make_cogs(self):
        """make dataframe including fasteners, attributes, forces and reserve factors"""
        cogs_dict = {
            "application_point_x": self.application_point.x_coord,
            "application_point_y": self.application_point.y_coord,
            "application_point_z": self.application_point.z_coord,
            "centroid_ys": self.fastener_group.centroid_ys,
            "centroid_zs": self.fastener_group.centroid_zs,
            "centroid_yt": self.fastener_group.centroid_yt,
            "centroid_zt": self.fastener_group.centroid_zt,
        }
        return cogs_dict


def create_dummmy_fastener(dummy_fast):
    """create dummy fastener as average for fasteners in compression"""

    dummy_fastener = Fastener(
        name="dummy_fastener",
        specification="dummy_fastener",
        x_coord=np.mean([fast.x_coord for fast in dummy_fast]),
        y_coord=max([fast.y_coord for fast in dummy_fast], key=abs),
        z_coord=np.mean([fast.z_coord for fast in dummy_fast]),
        shear_allowable=0.0001,
        tension_allowable=9999000,
    )

    return dummy_fastener


def iterate_calc(hsb21030_calc):
    """3.4 Additional forces due to the contact of the joined parts (compression)
    The fasteners considered above are loaded in tension only. Compressive forces are taken by
    contact of the joined parts (point C). If, after the first calculation, individual fasteners
    show negative tensile forces, a second calculation is required as follows:
    """

    # check if fasteners are in tension
    # if not, make dummy fastener and add to fastener group
    # create new fastener_group
    fasteners = hsb21030_calc.fastener_group.fasteners
    fastener_iter = []
    dummy_fast = []
    for i, tension in enumerate(hsb21030_calc.fastener_tension):
        if not tension[1]:
            dummy_fast_tmp = fasteners[i].copy()
            dummy_fast.append(dummy_fast_tmp)
            rep_fastener = fasteners[i]
            rep_fastener.__setattr__("tension_allowable", 0)
            fastener_iter.append(rep_fastener)

        else:
            fastener_iter.append(fasteners[i])

    dummy_fastener = create_dummmy_fastener(dummy_fast)
    fastener_iter += [dummy_fastener]
    fastener_group_iter = FastenerGroup(
        f"{hsb21030_calc.fastener_group.name}_iter", fastener_iter
    )

    iteration = Hsb2103001(
        name=f"{hsb21030_calc.name}_interation",
        fastener_group=fastener_group_iter,
        forces=hsb21030_calc.forces,
        moments=hsb21030_calc.moments,
        application_point=hsb21030_calc.application_point,
        reference_point=hsb21030_calc.reference_point,
    )

    print(f"NOTE: fastener {dummy_fastener.name} is added to fastener group")

    return iteration
