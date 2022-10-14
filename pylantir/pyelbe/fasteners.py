"""classes for fasteners"""
from dataclasses import dataclass, field
from collections import namedtuple
import copy
from array import array
import pandas as pd
import numpy as np

#TODO: move to pyelbe.py
# TODO: make coordinates into tuple
# pylint: disable=too-many-instance-attributes
@dataclass
class Fastener:
    """
    Class for fastener

    :param name: name of the fastener
    :type name: str
    :param specification: specification of the fastener
    :type specification: str
    :param shear_allowable: shear allowable of the fastener
    :type shear_allowable: float
    :param tension_allowable: tension allowable of the fastener
    :type tension_allowable: float
    :param x_coord: x coordinate of the fastener
    :type x_coord: float
    :param y_coord: y coordinate of the fastener
    :type y_coord: float
    :param z_coord: z coordinate of the fastener
    :type z_coord: float

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
    # TODO: make dummy fastener here
    def copy(self):
        """
        Copy fastener
        """
        return copy.deepcopy(self)


# TODO: make Fastenergroup from pd.DataFrame
# Class joint with fasteners
# combination fastener / plates

#TODO: move to pyelbe.py 
#TODO: FIX
#@dataclass
#class BoltedJoint:
#    """
#    Fastener / Material combination
#    material_name
#    bolt
#    thickness
#    shear_off
#    tension
#    head_ult
#    head_yield
#    nut_ult
#    nut_yield
#    """
#    name: str
#    fastener: Fastener
#    material_1: Material
#    material_2: Material
#    thickness_1: float
#    thickness_2: float
#    shear_allowable_1: float
#    shear_allowable_2: float
#    tension_allowable_1: float
#    tension_allowable_2: float
# TODO: calculate allowables according to bolted joint calcs


#TODO: move to pyelbe.py
@dataclass
class FastenerGroup:
    """
    Class for fastener group

    :param name: name of the fastener group
    :type name: str
    :param fasteners: list of fasteners in the fastener group
    :type fasteners: list
    :param fastener_names: list of fastener names in the fastener group
    :type fastener_names: list
    :param x_array: x coordinates of the fasteners in the fastener group
    :type x_array: list
    :param y_array: y coordinates of the fasteners in the fastener group
    :type y_array: list
    :param shear: shear allowables of the fasteners in the fastener group
    :type shear: list
    :param tension: tension allowables of the fasteners in the fastener group
    :type tension: list
    :param centroid_ys: y coordinate of the shear centroid of the fastener group
    :type centroid_ys: namedtuple
    :param centroid_yt: y coordinate of the tension centroid of the fastener group
    :type centroid_yt: namedtuple
    :param centroid_zs: z coordinate of the shear centroid of the fastener group
    :type centroid_zs: namedtuple
    :param centroid_zt: z coordinate of the tension centroid of the fastener group
    :type centroid_zt: namedtuple
    :param dataframe: dataframe of the fastener group
    :type dataframe: pandas dataframe

    """

    name: str
    fasteners: list
    fastener_names: list = field(init=False)
    x_array: array = field(init=False)
    y_array: array = field(init=False)
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

        # fastener names
        self.fastener_names = [fastener.name for fastener in self.fasteners]
        # X array from fasteners
        self.x_array = np.array([fastener.x_coord for fastener in self.fasteners])
        # Y array from fasteners
        self.y_array = np.array([fastener.y_coord for fastener in self.fasteners])
        # shear array from fasteners
        self.shear = np.array([fastener.shear_allowable for fastener in self.fasteners])
        # tension array from fasteners
        self.tension = np.array(
            [fastener.tension_allowable for fastener in self.fasteners]
        )

        self.centroid_ys = self.calculate_centroid_ys()
        self.centroid_zs = self.calculate_centroid_zs()

        # TODO: Calculation for tension assuming same material of rivets.
        # If different materials are used, use E for scaling

        self.centroid_yt = self.calculate_centroid_yt()
        self.centroid_zt = self.calculate_centroid_zt()

        # dataframe
        self.dataframe = self.create_dataframe()

    def calculate_centroid_ys(self) -> namedtuple:
        r"""
        Calculates centroid of fastener group in y direction

        :math:`y_{S} = \frac{\sum (F_{s,all,i}\cdot y_{i})}{\sum F_{s,all,i}}`
        """

        centroid_ys = sum(
            [fastener.y_coord * fastener.shear_allowable for fastener in self.fasteners]
        ) / sum([fastener.shear_allowable for fastener in self.fasteners])
        return centroid_ys

    def calculate_centroid_zs(self) -> namedtuple:
        r"""
        Calculates centroid of fastener group in z direction

        :math:`z_{S} = \frac{\sum (F_{s,all,i}\cdot z_{i})}{\sum F_{s,all,i}}`
        """
        centroid_zs = sum(
            [fastener.z_coord * fastener.shear_allowable for fastener in self.fasteners]
        ) / sum([fastener.shear_allowable for fastener in self.fasteners])
        return centroid_zs

    def calculate_centroid_yt(self) -> namedtuple:
        r"""
        Calculates centroid of fastener group in y direction,

        :math:`y_{T} = \frac{\sum (F_{t,all,i}\cdot y_{i})}{\sum F_{t,all,i}}`
        """
        # TODO: scaled by E

        centroid_yt = sum(
            [
                fastener.y_coord * fastener.tension_allowable
                for fastener in self.fasteners
            ]
        ) / sum([fastener.tension_allowable for fastener in self.fasteners])
        return centroid_yt

    def calculate_centroid_zt(self) -> namedtuple:
        r"""
        Calculates centroid of fastener group in z direction,

        :math:`z_{T} = \frac{\sum (F_{t,all,i}\cdot z_{i})}{\sum F_{t,all,i}}`
        """
        # TODO: scaled by E
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
