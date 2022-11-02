# -*- coding: utf-8 -*-

from math import pi, isclose
from collections import namedtuple
import pytest

from pylantir.pyelbe.hsb.hsb_profiles import LProfile
#import Material class
from pylantir.pyweser.matreel.material import Material

#test for LProfile class
def test_LProfile():
    """Test LProfile class"""

    # EXAMPLE from HSB 21030-01 Issue D 1978 (page 6)
    # L profile definition
    L = LProfile(
            b= 100,
            h= 100,
            profile_type= "extruded",
            t_fx= 2,
            t_fy= 2,
            radius = 4,
            mat_name = "S235",
            mat_spec = "S235JR",
            x_orig = 0,
            y_orig = 0
        )

    #material definition
    mat = Material(name="S235", specification="S235JR")

    assert L.b == 100
    assert L.h == 100
    assert L.profile_type == "extruded"
    assert L.t_fx == 2
    assert L.t_fy == 2
    assert L.radius == 4
    assert L.x_orig == 0
    assert L.y_orig == 0

    
    assert L.mat_list == ([mat, mat, mat])
    assert isclose(L.profile.x_cg, 25.55, abs_tol=0.01)
    assert isclose(L.profile.y_cg, 25.55, abs_tol=0.01)
    assert isclose(L.profile.Ixx, 406188, abs_tol=50)
    assert isclose(L.profile.Iyy, 406188, abs_tol=50)
    assert L.Ixx == L.profile.Ixx
    assert L.Iyy == L.profile.Iyy

    # L profile definition with bended profile type
    L = LProfile(
            b= 100,
            h= 100,
            profile_type= "bended",
            t_fx= 2,
            t_fy= 2,
            radius = 4,
            mat_name = "S235",
            mat_spec = "S235JR",
            x_orig = 0,
            y_orig = 0
        )  
    
    assert L.b == 100
    assert L.h == 100
    assert L.profile_type == "bended"
    assert L.t_fx == 2
    assert L.t_fy == 2
    assert L.radius == 4
    assert L.x_orig == 0
    assert L.y_orig == 0

    # calculated properties
    assert L.mat_list == ([mat, mat, mat])
    assert isclose(L.profile.x_cg, 26.03, abs_tol=0.01) #TODO: check this value: these should be the same!
    assert isclose(L.profile.y_cg, 26.03, abs_tol=0.01) #TODO: check this value: these should be the same!
    assert isclose(L.profile.Ixx, 401556, abs_tol=50)
    assert isclose(L.profile.Iyy, 401556, abs_tol=50)
    assert L.Ixx == L.profile.Ixx
    assert L.Iyy == L.profile.Iyy


    