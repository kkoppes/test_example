# -*- coding: utf-8 -*-

from collections import namedtuple
import pytest

from math import isclose
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
    x_array = [0, 0, 0, 0]
    y_array = [-70, -40, -40, -60]
    #Z = [35, 35, 15, 15] not used?

    shear = [18500, 18500, 18500, 18500]
    tension = [12000, 12000, 12000, 12000]
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
    assert (fastener_group.x_array == x_array).all()
    assert (fastener_group.y_array == y_array).all()
    assert (fastener_group.shear == shear).all()
    assert (fastener_group.tension == tension).all()
    assert fastener_group.centroid_ys == centroid_ys
    assert fastener_group.centroid_zs == centroid_zs
    assert fastener_group.centroid_yt == centroid_yt
    assert fastener_group.centroid_zt == centroid_zt
