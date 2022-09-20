from collections import namedtuple
from re import X
import pytest

from math import isclose
from src.pyelbe.hsb.hsb_21030_10 import (
    moment_x_reference,
    moment_x_reference_markdown,
    moment_y_reference,
    moment_y_reference_markdown,
    moment_z_reference,
    moment_z_reference_markdown,
    moments_transformation,
    ReferencePoint,
    Moments,
    Forces,
    Fastener,
    FastenerGroup,
    HSB_21030_01,
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


# def test_moments_transformation():
#    """Test moments_transformation"""#
#
#

#    reference_point = namedtuple("reference_point", "x_coord y_coord z_coord")
#    reference_point = reference_point(0, 0, 0)#

#    # test 1: call function with all 0 values, test type and value
#    assert moments_transformation(
#        moments_p, forces_p, application_point, reference_point
#    ) == (10, 10, 10)#

#    # test 2: call function with only unit values for moments and forces, test type and value
#    moments_p = namedtuple("moments_p", "moment_x moment_y moment_z")
#    moments_p = moments_p(1, 1, 1)#

#    forces_p = namedtuple("forces_p", "force_x force_y force_z")
#    forces_p = forces_p(1, 1, 1)#

#    application_point = namedtuple("application_point", "x_coord y_coord z_coord")
#    application_point = application_point(1, 1, 1)#

#    reference_point = namedtuple("reference_point", "x_coord y_coord z_coord")
#    reference_point = reference_point(0, 0, 0)#

#    assert moments_transformation(
#        moments_p, forces_p, application_point, reference_point
#    ) == (1, 1, 1)

# test for fastener class
def test_fastener():
    """Test fastener class"""

    # fastener 1 definition
    fastener = Fastener(
        name="test_name",
        specification="test_spec",
        material="test_mat",
        shear_allowable=1,
        tension_allowable=2,
        x_coord=3,
        y_coord=4,
        z_coord=5,
    )

    assert fastener.name == "test_name"
    assert fastener.specification == "test_spec"
    assert fastener.material == "test_mat"
    assert fastener.shear_allowable == 1
    assert fastener.tension_allowable == 2
    assert fastener.x_coord == 3
    assert fastener.y_coord == 4
    assert fastener.z_coord == 5


# test for fastener group class
def test_fastener_group():
    """Test fastener group class"""

    # EXAMPLE from HSB 21030-01 Issue D 1978 (page 6)
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

    # expected results for fastener group:
    X = [0, 0, 0, 0]
    Y = [-70, -40, -40, -60]
    Z = [35, 35, 15, 15]
    Shear = [18500, 18500, 18500, 18500]
    Tension = [12000, 12000, 12000, 12000]
    # HSB 21030-01 Issue D 1978 (page 7) 4.4
    centroid_ys = -52.5
    centroid_zs = 25
    centroid_yt = -52.5
    centroid_zt = 25

    # fastener group definition
    fastener_group = FastenerGroup(
        "test", [fastener_1, fastener_2, fastener_3, fastener_4]
    )
    assert fastener_group.name == "test"
    assert fastener_group.fasteners == [
        fastener_1,
        fastener_2,
        fastener_3,
        fastener_4,
    ]
    assert (fastener_group.X == X).all()
    assert (fastener_group.Y == Y).all()
    assert (fastener_group.shear == Shear).all()
    assert (fastener_group.tension == Tension).all()
    assert fastener_group.centroid_ys == centroid_ys
    assert fastener_group.centroid_zs == centroid_zs
    assert fastener_group.centroid_yt == centroid_yt
    assert fastener_group.centroid_zt == centroid_zt


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

    # HSB_21030_01
    HSB_calc = HSB_21030_01(
        id="HSB_21030_01",
        fastener_group=fastener_group,
        forces=forces,
        moments=moments,
        application_point=point_p,
        reference_point=point_u,
    )
    # forces, moments, point_p, point_u
    # )

    assert HSB_calc.id == "HSB_21030_01"
    # expected results:
    # HSB 21030-01 Issue D 1978 (page 7)
    # 4.3 Moments about point U
    MxU = -240000  # Nmm
    MyU = 260000  # Nmm
    MzU = 360000  # Nmm

    assert HSB_calc.moments_u == (MxU, MyU, MzU)

    # HSB 21030-01 Issue D 1978 (page 7) 4.4
    centroid_ys = -52.5
    centroid_zs = 25
    centroid_yt = -52.5
    centroid_zt = 25

    
    # HSB 21030-01 Issue D 1978 (page 7)
    # 4.4 Moments about the centroid of the fastener group
    MxS = -45000  # Nmm (Shear)
    MyS = 10000  # Nmm (Tension)
    MzS = -165000  # Nmm (Tension)

    assert HSB_calc.moment_x_s == MxS
    assert HSB_calc.moment_y_s == MyS
    assert HSB_calc.moment_z_s == MzS
    
    # HSB 21030-01 Issue D 1978 (page 8)
    # 4.6 Forces of individual fasteners
    # NOTE: HSB values are rounded to 2 decimal places for kN
    Fsy1 = 3420  # N
    Fsy2 = 3420  # N
    Fsy3 = 2580  # N
    Fsy4 = 2580  # N

    assert isclose(HSB_calc.force_fsy[0], Fsy1,  abs_tol=10) 
    assert isclose(HSB_calc.force_fsy[1], Fsy2,  abs_tol=10)
    assert isclose(HSB_calc.force_fsy[2], Fsy3,  abs_tol=10)
    assert isclose(HSB_calc.force_fsy[3], Fsy4,  abs_tol=10)

    Fsz1 = 230  # N
    Fsz2 = -1020  # N
    Fsz3 = -1020  # N
    Fsz4 = -190  # N

    assert isclose(HSB_calc.force_fsz[0], Fsz1,  abs_tol=10)
    assert isclose(HSB_calc.force_fsz[1], Fsz2,  abs_tol=10)
    assert isclose(HSB_calc.force_fsz[2], Fsz3,  abs_tol=10)
    assert isclose(HSB_calc.force_fsz[3], Fsz4,  abs_tol=10)
    
    Fs1 = 3430  # N
    Fs2 = 3570  # N
    Fs3 = 2780  # N
    Fs4 = 2590  # N

    assert isclose(HSB_calc.shear_forces[0], Fs1,  abs_tol=10)
    assert isclose(HSB_calc.shear_forces[1], Fs2,  abs_tol=10)
    assert isclose(HSB_calc.shear_forces[2], Fs3,  abs_tol=10)
    assert isclose(HSB_calc.shear_forces[3], Fs4,  abs_tol=10)

    Ft1 = -1120  # N
    Ft2 = 6620  # N
    Ft3 = 4830  # N
    Ft4 = -330  # N

    assert isclose(HSB_calc.tension_forces[0], Ft1,  abs_tol=10)
    assert isclose(HSB_calc.tension_forces[1], Ft2,  abs_tol=10)
    assert isclose(HSB_calc.tension_forces[2], Ft3,  abs_tol=10)
    assert isclose(HSB_calc.tension_forces[3], Ft4,  abs_tol=10)

    # pyelbe centers of gravity
    # expected results:

    centers_of_gravity = (
        point_p.x_coord,
        point_p.y_coord,
        point_p.z_coord,
        centroid_ys,
        centroid_zs,
        centroid_yt,
        centroid_zt
    )

    assert HSB_calc.cogs["application_point_x"] == centers_of_gravity[0]
    assert HSB_calc.cogs["application_point_y"] == centers_of_gravity[1]
    assert HSB_calc.cogs["application_point_z"] == centers_of_gravity[2]
    assert HSB_calc.cogs["centroid_ys"] == centers_of_gravity[3]
    assert HSB_calc.cogs["centroid_zs"] == centers_of_gravity[4]
    assert HSB_calc.cogs["centroid_yt"] == centers_of_gravity[5]
    assert HSB_calc.cogs["centroid_zt"] == centers_of_gravity[6]