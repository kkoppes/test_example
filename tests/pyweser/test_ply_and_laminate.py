#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 22 10:39:33 2022

@author: gi11883
"""

from pylantir.pyweser.matreel import Laminate, Ply, OrthoMaterial

name = "IMA_M21E_194_0.184"
spec = "IPS05-27-002-01"
E1 = 154e3
E2 = 8.5e3
G12 = 4.2e3
nu12 = 0.35
thickness = 0.184

mat_1 = OrthoMaterial(
    name=name, specification=spec, E1=E1, E2=E2, G12=G12, nu12=nu12
)


def test_ply() -> None:
    """test Ply class initialization, no errors shall occour"""
    angle = 45  # deg
    ply = Ply(material=mat_1, thickness=thickness, angle=angle)
    assert ply.angle == float(angle)
    assert ply.thickness == thickness


def test_laminate() -> None:
    """test Laminate class initialization, no errors shall occour"""
    # build the stacking
    angles = [0, 0, 90, 45, 45, 90, 0, 45, 45, 90, 0, 0]  # deg
    stacking = []
    for angle in angles:
        stacking += [Ply(material=mat_1, thickness=thickness, angle=angle)]
    laminate = Laminate(stacking=stacking)
    # pre-calculated laminate equivalent elastic properties
    Eeq1 = 72.300054e3
    Eeq2 = 48.026429e3
    Geq12 = 12.301211e3
    nueq12 = 0.110981
    # threshold 1e-6
    thd = 1e-6
    assert abs(laminate.thickness - len(angles) * thickness) < thd
    assert abs(laminate.nu12 - nueq12) < thd
    # threshold 1e-3
    thd = 1e-3
    assert abs(laminate.E1 - Eeq1) < thd
    assert abs(laminate.E2 - Eeq2) < thd
    assert abs(laminate.G12 - Geq12) < thd
    # check the stacking sequence 
    stacking_sequence = "[" + "/".join([ str(angle) for angle in angles]) + "]"
    assert str(laminate) == stacking_sequence
    assert len(laminate) == len(angles)


if __name__ == "__main__":
    test_ply()
    test_laminate()
