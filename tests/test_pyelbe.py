"""tests for pyelbe.py  """

import pytest

from pylantir.pyelbe.pyelbe import SubEl

def test_subel():
    """test SubEl class"""
    sub_type = "test"
    coords = (1, 2)
    subel = SubEl(sub_type, coords)
    assert subel is not None
    assert subel.sub_type == sub_type
    assert subel.position == coords
    assert subel.x == coords[0]
    assert subel.y == coords[1]


    #sub_type = "rect"
    #sub_type = "fillet"
    #sub_type = "qarc"
    #sub_type = "arc"