from math import pi, sqrt, isclose
import pytest
from pylantir.scrolls import get_logger

from pylantir.pyelbe.geometry_helpers import (
    area_rectangle,
    centroid_rectangle,
    inertia_rectangle,
    area_circle_sector,
    area_arc_sector,
    centroid_circle_sector,
    centroid_arc_sector,
    inertia_circle_sector,
    inertia_arc_sector
)

# set up logging
logger = get_logger(__name__)

# test for area of rectangle
def test_area_rectangle():
    """Test area of rectangle"""
    assert area_rectangle(1, 1) == 1
    assert area_rectangle(1, 2) == 2
    assert area_rectangle(2, 1) == 2
    assert area_rectangle(2, 2) == 4


# test for centroid of rectangle
def test_centroid_rectangle():
    """Test centroid of rectangle"""
    assert centroid_rectangle(1, 1) == (0.5, 0.5)
    assert centroid_rectangle(1, 2) == (0.5, 1.0)
    assert centroid_rectangle(2, 1) == (1.0, 0.5)
    assert centroid_rectangle(2, 2) == (1.0, 1.0)

    # test with rotation
    logger.debug("test with rotation")
    assert centroid_rectangle(1, 1, 45) == (0, sqrt(1 / 2))
    assert centroid_rectangle(1, 2, 45) == (-sqrt(1 / 2) / 2, (3 / 2) * sqrt(1 / 2))
    assert centroid_rectangle(2, 1, 45) == (sqrt(1 / 2) / 2, (3 / 2) * sqrt(1 / 2))
    assert centroid_rectangle(2, 2, 45) == (0, 2 * sqrt(1 / 2))

    # test 3nd quadrant
    logger.debug("test 3nd quadrant")
    C = centroid_rectangle(1, 1, 135)
    assert isclose(C.Cx, -sqrt(1 / 2), abs_tol=1e-6)
    assert isclose(C.Cy, 0, abs_tol=1e-6)
    C = centroid_rectangle(1, 2, 135)
    assert isclose(C.Cx, -(3 / 2) * sqrt(1 / 2), abs_tol=1e-6)
    assert isclose(C.Cy, -sqrt(1 / 2) / 2, abs_tol=1e-6)


def test_inertia_rectangle():
    """Test inertia of rectangle"""
    assert inertia_rectangle(1, 1) == (1 / 12, 1 / 12)
    assert inertia_rectangle(1, 2) == (1 * (8 / 12), 2 * (1 / 12))

    # rotate 45 degrees


# test for area of circle segment
def test_area_circle_sector():
    """Test area of circle segment"""
    assert area_circle_sector(1, 0, 360) == pi
    assert area_circle_sector(1, 0, 180) == pi / 2
    assert area_circle_sector(1, 0, 90) == pi / 4
    assert area_circle_sector(2, 0, 90) == pi
    assert area_circle_sector(3, 0, 90) == pi * 9 / 4
    assert area_circle_sector(1, 90, 270) == (1 / 2) * pi
    assert area_circle_sector(1, 90, 360) == (3 / 4) * pi
    assert area_circle_sector(1, 180, 270) == (1 / 4) * pi
    assert area_circle_sector(1, 180, 360) == (1 / 2) * pi
    assert area_circle_sector(1, 270, 360) == (1 / 4) * pi


# test for area of arc segment
def test_area_arc_sector():
    """Test area of arc segment"""
    test_radii = [1, 2]
    test_thicknesses = [1, 2]
    test_angles = [0, 90]
    test_angles_2 = [0, 90]

    answer_dictionary = {
        1: {
            1: {
                0: {0: 0, 90: 3 * pi / 4},
                90: {0: 3 * pi / 4, 90: 0},
            },
            2: {
                0: {0: 0, 90: 2 * pi},
                90: {0: 2 * pi, 90: 0},
            },
        },
        2: {
            1: {
                0: {0: 0, 90: 5 * pi / 4},
                90: {0: 5 * pi / 4, 90: 0},
            },
            2: {0: {0: 0, 90: 3 * pi}, 90: {0: 3 * pi, 90: 0}},
        },
    }

    for r in test_radii:
        logger.debug("r: %s", r)
        for t in test_thicknesses:
            logger.debug("t: %s", t)
            for a in test_angles:
                for b in test_angles_2:
                    logger.debug("a: %s", a)
                    logger.debug("b: %s", b)
                    area = area_arc_sector(r, t, a, b)
                    logger.debug("area: %s", area)
                    answer = answer_dictionary[r][t][a][b]
                    logger.debug("answer: %s", answer)
                    assert area == answer


# test for centroid of circle segment
def test_centroid_circle_sector():
    """Test centroid of circle segment"""
    logger.debug("test centroid of circle segment")
    centroid = centroid_circle_sector(1, 0, 360)
    answer = (0.0, 0.0)
    assert isclose(centroid[0], answer[0], abs_tol=1e-6)
    assert isclose(centroid[1], answer[1], abs_tol=1e-6)

    logger.debug("test centroid of half circle segment")
    centroid = centroid_circle_sector(1, 0, 180)
    answer = (0.0, 0.42)
    assert isclose(centroid[0], answer[0], abs_tol=1e-6)
    assert isclose(centroid[1], answer[1], abs_tol=0.01)

    logger.debug("test centroid of half circle segment on x axis")
    centroid = centroid_circle_sector(1, -90, 90)
    answer = (0.42, 0.0)
    assert isclose(centroid[0], answer[0], abs_tol=0.01)
    assert isclose(centroid[1], answer[1], abs_tol=0.01)

    logger.debug("test centroid of quarter circle segment")
    centroid = centroid_circle_sector(1, 0, 90)
    answer = (0.42, 0.42)
    assert isclose(centroid[0], answer[0], abs_tol=0.01)
    assert isclose(centroid[1], answer[1], abs_tol=0.01)


# test for centroid of arc segment
def test_centroid_arc_sector():
    """Test centroid of arc segment"""
    logger.debug("test centroid of arc segment")
    centroid = centroid_arc_sector(1,1, 0, 360)
    answer = (0.0, 0.0)

    assert isclose(centroid[0], answer[0], abs_tol=1e-6)
    assert isclose(centroid[1], answer[1], abs_tol=1e-6)
    logger.debug("test centroid of half arc segment")
    centroid = centroid_arc_sector(1,1, 0, 180)
    answer = (0.0, 0.99)
    assert isclose(centroid[0], answer[0], abs_tol=1e-6)
    assert isclose(centroid[1], answer[1], abs_tol=0.01)
    logger.debug("test centroid of half arc segment on x axis")
    centroid = centroid_arc_sector(1,1, -90, 90)
    answer = (0.99, 0.0)
    assert isclose(centroid[0], answer[0], abs_tol=0.01)
    assert isclose(centroid[1], answer[1], abs_tol=0.01)
    logger.debug("test centroid of quarter arc segment on x axis")
    centroid = centroid_arc_sector(1,1, -45, 45)
    answer = (1.40, 0.0)
    assert isclose(centroid[0], answer[0], abs_tol=0.01)
    assert isclose(centroid[1], answer[1], abs_tol=0.01)

def test_inertia_circle_sector():
    """Test inertia of circle segment"""
    logger.debug("test inertia of circle segment")
    Ix, Iy, Ixy = inertia_circle_sector(1, 0, 360)
    answer = (pi / 4, pi / 4)
    assert isclose(Ix, answer[0], abs_tol=1e-6)
    assert isclose(Iy, answer[1], abs_tol=1e-6)
    logger.debug("test inertia of half circle segment")
    Ix, Iy, Ixy = inertia_circle_sector(1, 0, 180)
    answer = (pi / 8, pi / 8)
    assert isclose(Ix, answer[0], abs_tol=1e-6)
    assert isclose(Iy, answer[1], abs_tol=1e-6)
    logger.debug("test inertia of half circle segment on x axis")
    Ix, Iy, Ixy = inertia_circle_sector(1, -90, 90)
    answer = (pi / 8, pi / 8)
    assert isclose(Ix, answer[0], abs_tol=1e-6)
    assert isclose(Iy, answer[1], abs_tol=1e-6)
    logger.debug("test inertia in cg of quarter circle segment")
    Ix, Iy, Ixy = inertia_circle_sector(1, 0, 90)
    answer = (pi / 16, pi / 16)
    assert isclose(Ix, answer[0], abs_tol=1e-6)
    logger.debug("test inertia in circle center of quarter circle segment")
    Ix, Iy, Ixy = inertia_circle_sector(1, 0, 90, cg=False)
    answer = (0.337, 0.337)
    assert isclose(Ix, answer[0], abs_tol=1e-3)
    
def test_inertia_arc_sector():
    """Test inertia of arc segment"""
    logger.debug("test inertia of arc segment")
    Ix, Iy, Ixy = inertia_arc_sector(1,1, 0, 360)
    answer = (11.780, 11.780)
    assert isclose(Ix, answer[0], abs_tol=1e-3)
    assert isclose(Iy, answer[1], abs_tol=1e-3)
    logger.debug("test inertia of half arc segment")
    Ix, Iy, Ixy = inertia_arc_sector(1,1, 0, 180, cg=True)
    answer = (14.756, 5.890)
    assert isclose(Ix, answer[0], abs_tol=1e-3)
    assert isclose(Iy, answer[1], abs_tol=1e-3)
    logger.debug("test inertia of half arc segment on x axis")
    Ix, Iy, Ixy = inertia_arc_sector(1,1, -90, 90)
    answer = (5.890, 5.890)
    assert isclose(Ix, answer[0], abs_tol=1e-3)
    assert isclose(Iy, answer[1], abs_tol=1e-3)
    logger.debug("test inertia in center of half arc segment on x axis")
    Ix, Iy, Ixy = inertia_arc_sector(1,1, 0, 90)
    answer = (pi / 8, pi / 8)
    assert isclose(Ix, answer[0], abs_tol=1e-6)
    assert isclose(Iy, answer[1], abs_tol=1e-6)