# -*- coding: utf-8 -*-

from math import pi, isclose
from collections import namedtuple
import pytest

from pylantir.pyelbe.profiles import SubEl, Profile, Rect, Arc, QArc, Fillet
from pylantir.pyweser.matreel.material import Material


def test_subel_init():
    """test class initialization no errors shall occour"""
    name = "test"
    subel = SubEl(name=name, pos_x=1, pos_y=1, mat_name="test", mat_spec="test", fc="red")
    assert subel.name == name
    assert subel.pos_x == 1
    assert subel.pos_y == 1
    assert subel.position == (1, 1)
    test_material = Material(name="test", specification="test")
    assert subel.material == test_material

    # assert with position as tuple
    subel = SubEl(name=name, position=(1, 1), mat_name="test", mat_spec="test")
    assert subel.name == name
    assert subel.pos_x == 1
    assert subel.pos_y == 1
    assert subel.position == (1, 1)
    test_material = Material(name="test", specification="test")
    assert subel.material == test_material

    # assert value error if no position or pos_x or pos_y is given
    with pytest.raises(ValueError):
        SubEl(name=name, mat_name="test", mat_spec="test")

    # assert logger warning if no material is given
    #with pytest.warns(UserWarning):
    #    SubEl(name=name, pos_x=1, pos_y=1, mat_name="test")



def test_subel_init_error():
    """test class initialization with error"""
    with pytest.raises(ValueError):
        SubEl()


# test class Rect
def test_rect_init():
    """test class initialization no errors shall occour"""
    name = "test"
    rect = Rect(
        name=name, pos_x=0, pos_y=0, mat_name="test", mat_spec="test", height=1, width=1
    )
    assert rect.name == name
    assert rect.pos_x == 0
    assert rect.pos_y == 0
    assert rect.position == (0, 0)
    test_material = Material(name="test", specification="test")
    assert rect.material == test_material
    assert rect.height == 1
    assert rect.width == 1

    # assert calculated properties
    assert rect.area == 1
    assert rect.xcg == 0.5
    assert rect.ycg == 0.5
    assert rect.Ixg == 1 / 12
    assert rect.Iyg == 1 / 12

    # test with angle
    rect = Rect(
        name=name,
        pos_x=0,
        pos_y=0,
        mat_name="test",
        mat_spec="test",
        height=1,
        width=1,
        angle=90,
    )
    assert rect.name == name
    assert rect.alpha == pi / 2
    assert isclose(rect.xcg, -0.5, abs_tol=0.01)
    assert isclose(rect.ycg, 0.5, abs_tol=0.01)
    assert isclose(rect.Ixg, 1 / 12, abs_tol=0.01)
    assert isclose(rect.Iyg, 1 / 12, abs_tol=0.01)

        # test with angle
    rect = Rect(
        name=name,
        pos_x=0,
        pos_y=0,
        mat_name="test",
        mat_spec="test",
        height=1,
        width=1,
        angle=45,
    )
    assert rect.name == name
    assert rect.alpha == pi / 4
    assert isclose(rect.xcg, 0, abs_tol=0.01)
    assert isclose(rect.ycg, 0.707, abs_tol=0.01)
    assert isclose(rect.Ixg, 1 / 12, abs_tol=0.01)
    assert isclose(rect.Iyg, 1 / 12, abs_tol=0.01)

        # test with angle
    rect = Rect(
        name=name,
        pos_x=0,
        pos_y=0,
        mat_name="test",
        mat_spec="test",
        height=1,
        width=1,
        angle=10,
    )
    assert rect.name == name
    assert rect.alpha == pi / 18
    assert isclose(rect.xcg, 0.4, abs_tol=0.01)
    assert isclose(rect.ycg, 0.58, abs_tol=0.01)
    assert isclose(rect.Ixg, 1 / 12, abs_tol=0.01)
    assert isclose(rect.Iyg, 1 / 12, abs_tol=0.01)

# test class Arc
def test_arc_init():
    """test class initialization no errors shall occour"""
    name = "test"
    arc = Arc(
        name=name,
        pos_x=0,
        pos_y=0,
        mat_name="test",
        mat_spec="test",
        outer_radius=2,
        inner_radius=1,
        angle=180,
    )
    assert arc.name == name
    assert arc.pos_x == 0
    assert arc.pos_y == 0
    assert arc.position == (0, 0)
    test_material = Material(name="test", specification="test")
    assert arc.material == test_material

    # assert calculated properties
    assert arc.area == 1.5 * pi
    assert isclose(arc.xcg, 0, abs_tol=0.01)
    assert isclose(arc.ycg, 0.99, abs_tol=0.01)

    assert isclose(arc.Ixg, 5.890, abs_tol=0.01)
    assert isclose(arc.Iyg, 5.890, abs_tol=0.01)

    #TODO: add rotation


# test class QArc
def test_qarc_init():
    """test class initialization no errors shall occour """
    name = "test"
    qarc = QArc(
        name=name,
        pos_x=0,
        pos_y=0,
        mat_name="test",
        mat_spec="test",
        outer_radius=2,
        inner_radius=1,
        beta=45,
    )
    assert qarc.name == name
    assert qarc.pos_x == 0
    assert qarc.pos_y == 0
    assert qarc.position == (0, 0)
    test_material = Material(name="test", specification="test")
    assert qarc.material == test_material

    # assert calculated properties
    assert qarc.area == 0.75 * pi   
    assert isclose(qarc.xcg, 0.99, abs_tol=0.01)
    assert isclose(qarc.ycg, 0.99, abs_tol=0.01)
    assert isclose(qarc.Ixx, 2.94, abs_tol=0.01)
    assert isclose(qarc.Iyy, 2.94, abs_tol=0.01)


# test class Fillet
def test_fillet_init():
    """test class initialization no errors shall occour"""
    name = "test"
    fillet = Fillet(
        name=name, pos_x=0, pos_y=0, mat_name="test", mat_spec="test", radius=1
    )
    assert fillet.name == name
    assert fillet.pos_x == 0
    assert fillet.pos_y == 0
    assert fillet.position == (0, 0)
    test_material = Material(name="test", specification="test")
    assert fillet.material == test_material

    # assert calculated properties
    assert isclose(fillet.area, 0.214, abs_tol=0.01)
    assert fillet.xcg == 0.5
    assert fillet.ycg == 0.5
    assert isclose(fillet.Ixg, 0, abs_tol=0.01)
    assert isclose(fillet.Iyg, 0, abs_tol=0.01)


# test class Profile
def test_profile_init():
    """test class initialization no errors shall occour"""
    name = "test"
    rect_1 = Rect(
        sub_type="rect", width=9, height=1, pos_x=1, pos_y=99, material="test"
    )
    rect_2 = Rect(
        sub_type="rect", width=1, height=100, pos_x=0, pos_y=0, material="test"
    )
    rect_3 = Rect(
        sub_type="rect", width=9, height=1, pos_x=-9, pos_y=0, material="test"
    )


    profile = Profile([rect_1, rect_2, rect_3], name=name)
    assert profile.name == name
    assert profile.subel_list == [rect_1, rect_2, rect_3]

    # assert calculated properties, checked with ISAMI IA1140_A350
    assert profile.area == 118
    assert profile.x_cg == 0.5
    assert profile.y_cg == 50
    
    assert round(profile.Ixg, 0) == 127439
    assert round(profile.Iyg) == 580

    assert round(profile.Ixx, 0) == 422439
    assert round(profile.Iyy, 0) == 609



    