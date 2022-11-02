#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Laminate is a `pyweser.matreel` module for the modelling of laminated materials.
"""
# import pdb
from dataclasses import dataclass
from typing import Union
import numpy as np
from pylantir.pyweser.matreel import OrthoMaterial


@dataclass(slots=True)
class Ply:
    """.. _Ply:

    Class to represent a ply made of an orthotropic material.

    :param material: orthotropic material
    :type material: OrthoMaterial_

    :param thickness: thickness of the ply
    :type thickness: float

    :param angle: orientation of the ply in **degrees**
    :type angle: int, float

    """

    material: OrthoMaterial
    thickness: float
    angle: float

    @property
    def Q_0(self) -> np.array:
        """
        Lamina stiffness matrix along the 1st direction (0 degrees)

        :type: `numpy.array`
        """
        material = self.material
        E1 = material.E1
        E2 = material.E2
        nu12 = material.nu12
        nu21 = nu12 * E2 / E1
        pois = 1 - nu12 * nu21
        Q11 = E1 / pois
        Q12 = nu12 * E2 / pois
        Q21 = Q12
        Q22 = E2 / pois
        Q66 = material.G12
        return np.array([[Q11, Q12, 0], [Q21, Q22, 0], [0, 0, Q66]])

    @property
    def Q_a(self) -> np.array:
        """
        Rotated stiffness matrix at the ply angle.

        :type: `numpy.array`
        """
        angle = self.angle * np.pi / 180.0
        cos_a = np.cos(angle)
        sin_a = np.sin(angle)
        v_1 = [cos_a**2, sin_a**2, -2 * cos_a * sin_a]
        v_2 = [sin_a**2, cos_a**2, 2 * cos_a * sin_a]
        v_3 = [cos_a * sin_a, -cos_a * sin_a, cos_a**2 - sin_a**2]
        rot = np.array([v_1, v_2, v_3])
        return np.matmul(rot, np.matmul(self.Q_0, rot.T))


class Laminate:
    """.. _Laminate:

    Class to represent laminated materials.

    :param stacking: stacking sequence
    :type stacking: list of Ply_
    """

    __slots__ = (
        "__stacking",
        "__matrices",
        "__nu12",
        "__K",
        "__invK",
        "__z",
    )

    def __init__(self, stacking: list[Ply]):
        """Constructor method"""
        self.__z = np.array([0.0])
        self.stacking = stacking
        A = []
        B = []
        D = []
        self.__matrices = [[A, B], [B, D]]
        self.__calc_matrices()

    def __getitem__(self, ith: int) -> Ply:
        """Get the ith ply in the stacking."""
        return self.__stacking[ith - 1]

    def __iter__(self) -> iter:
        """Iterate through the stacking list."""
        return iter(self.__stacking)

    def __len__(self) -> int:
        """Calling len(Laminate) return the number of plies."""
        return self.n_plies

    def __repr__(self) -> str:
        """
        Return the stacking angle sequence as a string when printed.

        :return: the stacking in the form [0, 45, 90, ..., 90, -45, 0]
        :rtype: str
        """
        string = [""] * self.n_plies
        for ind, ply in enumerate(self.__stacking):
            string[ind] = f"{ply.angle:d}"
        return "[" + "/".join(string) + "]"

    @property
    def thickness(self) -> float:
        """
        Laminate thickness.

        :type: float
        """
        return self.__z[-1] * 2.0

    @property
    def stacking(self) -> list[Ply]:
        """
        Stacking sequence.

        :setter: set the stacking sequence
        :getter: get the stacking sequence
        :type: list of Ply_
        """
        return self.__stacking

    @stacking.setter
    def stacking(self, stacking: list[Ply]) -> None:
        """Store the stacking sequence, and build the symmetric thicknesses
        sequence, checking that each ply is a matreel Ply object.
        """
        # check that the input is a list of Ply
        match stacking:
            case list():
                pass
            case _:
                raise TypeError(
                    " the argument 'stacking' must be a list of class Ply"
                )
        # build-up the thicknesses sequence, the bottom ply is first ply
        self.__z = [0.0]
        for ind, ply in enumerate(stacking):
            layer = ind + 1
            if not isinstance(ply, Ply):
                raise TypeError(
                    f" the argument 'stacking' must be a list of class Ply, ply #{layer} is {type(ply)}."
                )
            self.__z.append(self.__z[-1] + ply.thickness)
        # make the sequence symmetric in respect with the laminate midline
        self.__z = np.array(self.__z) - self.__z[-1] * 0.5
        # duplicate the argument and store it into the class
        self.__stacking = list(stacking)

    @property
    def A(self) -> np.array:
        """
        Extensional stiffness matrix A.

        :type: np.array
        """
        return self.__matrices[0][0]

    @property
    def B(self) -> np.array:
        """
        Coupling stiffness matrix B.

        :type: np.array
        """
        return self.__matrices[0][1]

    @property
    def D(self) -> np.array:
        """
        Bending stiffness matrix D.

        :type: np.array
        """
        return self.__matrices[1][1]

    @property
    def K(self) -> np.array:
        """
        Laminate full stiffness matrix.

        :type: np.array
        """
        return self.__K

    @property
    def invK(self) -> np.array:
        """
        Laminate compliance matrix :math:`K^{-1}`

        :type: np.array
        """
        return self.__invK

    @property
    def n_plies(self) -> int:
        """
        Number of plies.

        :type: int
        """
        return len(self.__stacking)

    @property
    def E1(self) -> float:
        """
        Laminate equivalent Young's modulus along direction 1.

        :type: float
        """
        return 1.0 / self.__invK.item(0, 0) / self.thickness

    @property
    def E2(self) -> float:
        """
        Laminate equivalent Young's modulus along direction 2.

        :type: float
        """
        return 1.0 / self.__invK.item(1, 1) / self.thickness

    @property
    def G12(self) -> float:
        """
        Laminate equivalent the shear modulus in the plane 1-2.

        :type: float
        """
        return 1.0 / self.__invK.item(2, 2) / self.thickness

    @property
    def nu12(self) -> float:
        """Laminate equivalent Poisson's ratio in the plane 1-2.

        :type: float
        """
        return self.__nu12

    def Q(self, ith: int) -> Union[np.array, None]:
        """:method: calculate the :math:`i_{th}` ply stiffness matrix along the ply angle.

        :param ith: ply number
        :type ith: int

        :return: ply stiffness matrix Q
        :rtype: :class:`numpy.array` or None
        """
        return self.__stacking[ith - 1].Q_a

    def __calc_matrices(self) -> None:
        """Private method to compute the laminate stiffness matrices"""
        # ref. NASA RP-1351
        A = np.zeros([3, 3])
        B = np.zeros([3, 3])
        D = np.zeros([3, 3])
        for layer in range(self.n_plies):
            z_1 = self.__z[layer]
            z_2 = self.__z[layer + 1]
            Qrot = self.Q(layer + 1)
            A += Qrot * (z_2 - z_1)
            B += Qrot * (z_2**2 - z_1**2) / 2.0
            D += Qrot * (z_2**3 - z_1**3) / 3.0
        self.__matrices = [[A, B], [B, D]]
        self.__K = np.block(self.__matrices)
        self.__invK = np.linalg.inv(self.__K)
        self.__nu12 = self.__calc_poisson()

    def __calc_poisson(self) -> float:
        """Private method to compute the equivalent Poisson's ratio nu12"""
        # ref. NASA RP-1351l
        # nu12 = - detK_12 / detK_11
        # where detK_11 is calculated as
        # get the stiffness matrix K
        detK_11 = np.array(self.__K)
        # remove the first row and first column
        detK_11 = np.delete(detK_11, 0, 0)
        detK_11 = np.delete(detK_11, 0, 1)
        # compute the determinant
        detK_11 = np.linalg.det(detK_11)
        # and where detK_12 is calculated as
        # get the stiffness matrix K
        detK_12 = np.array(self.__K)
        # remove the first row and second column
        detK_12 = np.delete(detK_12, 0, 0)
        detK_12 = np.delete(detK_12, 1, 1)
        # compute the determinant
        detK_12 = np.linalg.det(detK_12)
        # return the absolute value of the ratio to ensure nu12 > 0
        return np.abs(detK_12 / detK_11)
