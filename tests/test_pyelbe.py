import pytest
from src.pyelbe.hsb.hsb_21030_10 import moment_x_reference


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

    # test 6: call function with strings, test type and value
    # TODO: does not work, add exception handling
    assert moment_x_reference("1", "1", "1", "1", "1") == 4
    