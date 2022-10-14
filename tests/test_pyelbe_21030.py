# -*- coding: utf-8 -*-

from collections import namedtuple
import pytest

from math import isclose
from pylantir.pyelbe.hsb.hsb_21030_10 import (
    Hsb2103001,
)
from pylantir.pyelbe.loads import (
    Moments,
    Forces,
)
from pylantir.pyelbe.abstractions import (
    ReferencePoint
)
from pylantir.pyelbe.fasteners import (
    Fastener,
    FastenerGroup,
)

from pylantir.pyelbe.hsb.hsb_formulas import (
    moment_x_reference_markdown,
    moment_y_reference_markdown,
    moment_z_reference_markdown,
    moment_x_reference,
    moment_y_reference,
    moment_z_reference,
    moments_transformation,
)


def test_moment_x_reference():
    """Test moment_x_reference"""
    # test 1: call function with all 0 values, test type and value
    assert moment_x_reference(0, 0, 0, 0, 0) == 0
    assert type(moment_x_reference(0, 0, 0, 0, 0)) == float

    # test 2: call function only unit value for moment_x, test type and value
    assert moment_x_reference(1, 0, 0, 0, 0) == 1
    assert type(moment_x_reference(1, 0, 0, 0, 0)) == float
    # test 3: call function with moment_x realistic value, test value
    assert moment_x_reference(100, 0, 0, 0, 0) == 100

    # test 4: call function with only unit value for force_y and z_coord_p, test value
    assert moment_x_reference(0, 1, 0, 1, 0) == -1

    # test 5: call function with realistic values for force_y and z_coord_p, test value
    assert moment_x_reference(0, 100, 0, 100, 0) == -10000

    # test 6: : call function with only unit value for force_z and y_coord_p, test value
    assert moment_x_reference(0, 0, 1, 0, 1) == 1

    # test 7 test with reference coordinates
    assert moment_x_reference(1, 1, 1, 1, 1, 1, 1) == 1  # (cancel each other out)

    # test 9 test with reference y coordinates only
    assert moment_x_reference(1, 1, 1, 0, 0, 0, 1) == 0  # (negative)

    # test 8 test with reference coordinates only
    assert moment_x_reference(1, 1, 1, 0, 0, 1, 0) == 2  # (positive)

    # test 8 test with reference coordinates only
    assert moment_x_reference(1, 1, 1, 0, 0, 1, 1) == 1  # (they cancel each other out)

    # test 6: call function with strings, test type and value
    # TODO: does not work, add exception handling
    # assert moment_x_reference("1", 0, 0, 0, 0) == 4
    # assert moment_x_reference(0, "1", 0, "1", 0) == 4
    # assert moment_x_reference(0, 0, "1", 0, "1") == 4
    # TODO: test for
    # #moment_mxs = moment_mxu + forces[1] * cg_zs - forces[2] * cg_ys


def test_moment_x_reference_markdown():
    """Test moment_x_reference_markdown"""

    _, md_f = moment_x_reference_markdown(0, 0, 0, 0, 0)

    # test 1: call function with all 0 values, test type and value
    assert md_f == """$$0.0 = 0 - 0 \cdot (0 - 0) + 0 \cdot (0 - 0)$$"""
    assert type(md_f) == str


def test_moment_y_reference():
    """Test moment_y_reference"""
    # test 1: call function with all 0 values, test type and value
    assert moment_y_reference(0, 0, 0, 0, 0) == 0
    assert type(moment_y_reference(0, 0, 0, 0, 0)) == float

    # test 2: call function only unit value for moment_y, test type and value
    assert moment_y_reference(1, 0, 0, 0, 0) == 1
    assert type(moment_y_reference(1, 0, 0, 0, 0)) == float
    # test 3: call function with moment_y realistic value, test value
    assert moment_y_reference(100, 0, 0, 0, 0) == 100

    # test 4: call function with only unit value for force_z and x_coord_p, test value
    assert moment_y_reference(0, 0, 1, 1, 0) == -1

    # test 5: call function with realistic values for force_z and x_coord_p, test value
    assert moment_y_reference(0, 0, 100, 100, 0) == -10000

    # test 6: : call function with only unit value for force_x and z_coord_p, test value
    assert moment_y_reference(0, 1, 0, 0, 1) == 1
    # TODO: test for
    # moment_mys = moment_myu - forces[0] * cg_zt


def test_moment_y_reference_markdown():
    """Test moment_y_reference_markdown"""

    _, md_f = moment_y_reference_markdown(0, 0, 0, 0, 0)

    # test 1: call function with all 0 values, test type and value
    assert md_f == """$$0.0 = 0 + 0 \cdot (0 - 0) - 0 \cdot (0 - 0)$$"""
    assert type(md_f) == str


def test_moment_z_reference():
    """Test moment_z_reference"""
    # test 1: call function with all 0 values, test type and value
    assert moment_z_reference(0, 0, 0, 0, 0) == 0
    assert type(moment_z_reference(0, 0, 0, 0, 0)) == float

    # test 2: call function only unit value for moment_z, test type and value
    assert moment_z_reference(1, 0, 0, 0, 0) == 1
    assert type(moment_z_reference(1, 0, 0, 0, 0)) == float
    # test 3: call function with moment_z realistic value, test value
    assert moment_z_reference(100, 0, 0, 0, 0) == 100

    # test 4: call function with only unit value for force_x and y_coord_p, test value
    assert moment_z_reference(0, 1, 0, 0, 1) == -1

    # test 5: call function with realistic values for force_x and y_coord_p, test value
    assert moment_z_reference(0, 100, 0, 0, 100) == -10000

    # test 6: : call function with only unit value for force_y and x_coord_p, test value
    assert moment_z_reference(0, 0, 1, 1, 0) == 1

    # test for
    # moment_mzs = moment_mzu + forces[0] * cg_yt


def test_moment_z_reference_markdown():
    """Test moment_z_reference_markdown"""

    _, md_f = moment_z_reference_markdown(0, 0, 0, 0, 0)

    # test 1: call function with all 0 values, test type and value
    assert md_f == """$$0.0 = 0 - 0 \cdot (0 - 0) + 0 \cdot (0 - 0)$$"""
    assert type(md_f) == str


def test_integration():
    """
    integration test using the HSB example
    """

    # point P definition
    point_p = ReferencePoint(name="P", x_coord=30, y_coord=0, z_coord=0)

    # point U definition
    point_u = ReferencePoint(name="P", x_coord=0, y_coord=0, z_coord=0)

    # Load definition
    # force around P
    # Forces = namedtuple("Forces", "force_x force_y force_z")
    forces = Forces(name="forces", force_x=10000, force_y=12000, force_z=-2000)

    # Moment around U
    moments = Moments(name="moments", moment_x=-240000, moment_y=200000, moment_z=0)

    # fastener 1 definition
    # fastener_1 = Fastener("fast1", "test", "test", 1, 1, 1, 1, 0, -70, 35)
    fastener_1 = Fastener(
        name="fast1",
        specification="test",
        material="test",
        shear_allowable=18500,
        tension_allowable=12000,
        x_coord=0,
        y_coord=-70,
        z_coord=35,
    )

    # fastener 2 definition
    # fastener_2 = Fastener("fast2", "test", "test", 1, 1, 1, 1, 0, -40, 35)
    fastener_2 = Fastener(
        name="fast2",
        specification="test",
        material="test",
        shear_allowable=18500,
        tension_allowable=12000,
        x_coord=0,
        y_coord=-40,
        z_coord=35,
    )

    # fastener 3 definition
    # fastener_3 = Fastener("fast3", "test", "test", 1, 1, 1, 1, 0, -40, 15)
    fastener_3 = Fastener(
        name="fast3",
        specification="test",
        material="test",
        shear_allowable=18500,
        tension_allowable=12000,
        x_coord=0,
        y_coord=-40,
        z_coord=15,
    )

    # fastener 4 definition
    # fastener_4 = Fastener("fast4", "test", "test", 1, 1, 1, 1, 0, -60, 15)
    fastener_4 = Fastener(
        name="fast4",
        specification="test",
        material="test",
        shear_allowable=18500,
        tension_allowable=12000,
        x_coord=0,
        y_coord=-60,
        z_coord=15,
    )

    # fastener group definition
    fastener_group = FastenerGroup(
        name="test", fasteners=[fastener_1, fastener_2, fastener_3, fastener_4]
    )

    # Hsb2103001
    hsb_calc = Hsb2103001(
        name="Hsb2103001",
        fastener_group=fastener_group,
        forces=forces,
        moments=moments,
        application_point=point_p,
        reference_point=point_u,
    )
    # forces, moments, point_p, point_u
    # )

    assert hsb_calc.name == "Hsb2103001"
    # expected results:
    # HSB 21030-01 Issue D 1978 (page 7)
    # 4.3 Moments about point U
    mxu = -240000  # Nmm
    myu = 260000  # Nmm
    mzu = 360000  # Nmm

    assert hsb_calc.moments_u == (mxu, myu, mzu)

    # HSB 21030-01 Issue D 1978 (page 7) 4.4
    centroid_ys = -52.5
    centroid_zs = 25
    centroid_yt = -52.5
    centroid_zt = 25

    assert hsb_calc.fastener_group.centroid_ys == centroid_ys
    assert hsb_calc.fastener_group.centroid_zs == centroid_zs
    assert hsb_calc.fastener_group.centroid_yt == centroid_yt
    assert hsb_calc.fastener_group.centroid_zt == centroid_zt
    
    # HSB 21030-01 Issue D 1978 (page 7)
    # 4.4 Moments about the centroid of the fastener group
    mxs = -45000  # Nmm (shear)
    mys = 10000  # Nmm (tension)
    mzs = -165000  # Nmm (tension)

    assert hsb_calc.moment_x_s == mxs
    assert hsb_calc.moment_y_s == mys
    assert hsb_calc.moment_z_s == mzs

    # HSB 21030-01 Issue D 1978 (page 8)
    # 4.6 Forces of individual fasteners
    # NOTE: HSB values are rounded to 2 decimal places for kN
    fsy1 = 3420  # N
    fsy2 = 3420  # N
    fsy3 = 2580  # N
    fsy4 = 2580  # N

    assert isclose(hsb_calc.force_fsy[0], fsy1, abs_tol=10)
    assert isclose(hsb_calc.force_fsy[1], fsy2, abs_tol=10)
    assert isclose(hsb_calc.force_fsy[2], fsy3, abs_tol=10)
    assert isclose(hsb_calc.force_fsy[3], fsy4, abs_tol=10)

    fsz1 = 230  # N
    fsz2 = -1020  # N
    fsz3 = -1020  # N
    fsz4 = -190  # N

    assert isclose(hsb_calc.force_fsz[0], fsz1, abs_tol=10)
    assert isclose(hsb_calc.force_fsz[1], fsz2, abs_tol=10)
    assert isclose(hsb_calc.force_fsz[2], fsz3, abs_tol=10)
    assert isclose(hsb_calc.force_fsz[3], fsz4, abs_tol=10)

    fs1 = 3430  # n
    fs2 = 3570  # n
    fs3 = 2780  # n
    fs4 = 2590  # n

    assert isclose(hsb_calc.shear_forces[0], fs1, abs_tol=10)
    assert isclose(hsb_calc.shear_forces[1], fs2, abs_tol=10)
    assert isclose(hsb_calc.shear_forces[2], fs3, abs_tol=10)
    assert isclose(hsb_calc.shear_forces[3], fs4, abs_tol=10)

    ft1 = -1120  # n
    ft2 = 6620  # n
    ft3 = 4830  # n
    ft4 = -330  # n

    assert isclose(hsb_calc.tension_forces[0], ft1, abs_tol=10)
    assert isclose(hsb_calc.tension_forces[1], ft2, abs_tol=10)
    assert isclose(hsb_calc.tension_forces[2], ft3, abs_tol=10)
    assert isclose(hsb_calc.tension_forces[3], ft4, abs_tol=10)

    # pyelbe centers of gravity
    # expected results:

    centers_of_gravity = (
        point_p.x_coord,
        point_p.y_coord,
        point_p.z_coord,
        centroid_ys,
        centroid_zs,
        centroid_yt,
        centroid_zt,
    )

    assert hsb_calc.cogs["application_point_x"] == centers_of_gravity[0]
    assert hsb_calc.cogs["application_point_y"] == centers_of_gravity[1]
    assert hsb_calc.cogs["application_point_z"] == centers_of_gravity[2]
    assert hsb_calc.cogs["centroid_ys"] == centers_of_gravity[3]
    assert hsb_calc.cogs["centroid_zs"] == centers_of_gravity[4]
    assert hsb_calc.cogs["centroid_yt"] == centers_of_gravity[5]
    assert hsb_calc.cogs["centroid_zt"] == centers_of_gravity[6]
