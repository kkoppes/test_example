#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 22 10:17:15 2022

@author: gi11883
"""

from pylantir.pyweser.matreel import OrthoMaterial

def test_ortho_material_init() -> None:
    """test class initialization no errors shall occour"""
    name = "IMA_M21E_194_0.184"
    spec = "IPS05-27-002-01"
    E1 = 154e3
    E2 = 8.5e3
    E3 = 8.5e3
    G12 = 4.2e3
    G13 = 4.2e3
    G23 = 3.36e3
    nu12 = 0.35
    nu13 = 0.35
    nu23 = 0.26488095
    ortho = OrthoMaterial(
        name=name,
        specification=spec,
        E1=E1,
        E2=E2,
        E3=E3,
        G12=G12,
        G13=G13,
        G23=G23,
        nu12=nu12,
        nu13=nu13,
        nu23=nu23,
    )
    assert ortho.name == name
    assert ortho.specification == spec
    assert ortho.E1 == E1
    assert ortho.E2 == E2
    assert ortho.E3 == E3
    assert ortho.G12 == G12
    assert ortho.G13 == G13
    assert ortho.G23 == G23
    assert ortho.nu12 == nu12
    assert ortho.nu13 == nu13
    assert ortho.nu23 == nu23

    # provide arguments
    ortho = OrthoMaterial(
        name=name,
        specification=spec,
        E1=E1,
        E2=E2,
        G12=G12,
        nu12=nu12,
    )
    assert ortho.E1 == E1
    assert ortho.E2 == E2
    assert ortho.E3 == 0.0
    assert ortho.G12 == G12
    assert ortho.G13 == 0.0
    assert ortho.G23 == 0.0
    assert ortho.nu12 == nu12
    assert ortho.nu13 == 0.0
    assert ortho.nu23 == 0.0


if __name__ == "__main__":
    test_ortho_material_init()
