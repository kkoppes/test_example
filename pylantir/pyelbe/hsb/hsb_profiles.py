"""hsb profiles extention for pyelbe"""
from dataclasses import dataclass, field
from pylantir.scrolls import logging

from pylantir.pyelbe.profiles import Profile, Rect, Arc, QArc, Fillet

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
    radius: float = field(default=0)
    mat_name: str = field(default=None)
    mat_spec: str = field(default=None)
    x_orig: float = field(default=0)
    y_orig: float = field(default=0)
    
    def __post_init__(self, *args, **kwargs):
        """Init function for LProfile class"""

        if self.profile_type == "extruded":
            self.t_fy = self.t_fy
        elif self.profile_type == "bended":
            self.t_fy = self.t_fx

        if self.radius is None and self.profile_type == "bended":
            logging.warning(
                "No radius defined for bended profile, radius is set to 2 t"
            )
            self.radius = 2 * self.t_fx

        if self.radius is None and self.profile_type == "extruded":
            logging.warning(
                "No radius defined for extruded profile, radius is set to 2 * t_fx"
            )
            self.radius = 2 * self.t_fx

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
                    pos_x=self.x_orig,
                    pos_y=self.y_orig,
                    mat_name = self.mat_name,
                    mat_spec = self.mat_spec,
                    angle=0,
                )
            )

            subel_list.append(
                Rect(
                    width=self.t_fy,
                    height=self.h,
                    pos_x=self.x_orig,
                    pos_y=self.y_orig,
                    mat_name = self.mat_name,
                    mat_spec = self.mat_spec,
                )
            )
            subel_list.append(
                Fillet(
                    pos_x=self.x_orig + self.t_fx / 2,
                    pos_y=self.y_orig + self.t_fy / 2,
                    mat_name = self.mat_name,
                    mat_spec = self.mat_spec,
                    radius=self.radius,
                )
            )

        elif self.profile_type == "bended":
            # build up list from 2 rect and 1 qarc
            
            subel_list.append(
                Rect(
                    width=self.b - self.t_fy - self.radius,
                    height=self.t_fx,
                    pos_x=self.x_orig + self.t_fx + self.radius,
                    pos_y=self.y_orig,
                    mat_name = self.mat_name,
                    mat_spec = self.mat_spec,
                )
            )
            subel_list.append(
                Rect(
                    width=self.t_fy,
                    height=self.h - self.t_fx - self.radius,
                    pos_x=self.x_orig,
                    pos_y=self.y_orig + self.t_fy + self.radius,
                    mat_name = self.mat_name,
                    mat_spec = self.mat_spec,
                )
            )
            subel_list.append(
                QArc(
                    outer_radius=self.radius + self.t_fx,
                    inner_radius=self.radius,
                    pos_x=self.x_orig + self.t_fy + self.radius,
                    pos_y=self.y_orig + self.t_fx + self.radius,
                    mat_name = self.mat_name,
                    mat_spec = self.mat_spec,
                    beta=180               
                )
            )

        return subel_list
    
    #TODO: add average width of section depending on support

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
    def material(self):
        """Material of the profile"""
        return self.profile.material
    
    @property
    def mat_list(self):
        """Material of the profile"""
        return self.profile.mat_list

    