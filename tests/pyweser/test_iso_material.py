# -*- coding: utf-8 -*-

from pylantir.pyweser.matreel import IsoMaterial
import pytest


def calc_shear_modulus(E: float, nu: float) -> float:
    return E / 2.0 / (1.0 + nu)


def calc_poisson_ratio(E: float, G: float) -> float:
    return E / 2.0 / G - 1.0


def test_iso_material_init() -> None:
    """test class initialization no errors shall occour"""
    name = "Ti-6Al-4V_ab_Annealed_Plate"
    spec = "AIMS03-18-006"
    E = 110.3e3
    G = 42.75e3
    nu = 310e-3
    iso = IsoMaterial(
        name=name,
        specification=spec,
        E=E,
        G=G,
        nu=nu,
    )
    assert iso.name == name
    assert iso.specification == spec
    assert iso.E == E
    assert iso.G == G
    assert iso.nu == nu

    iso = IsoMaterial(
        name=name,
        specification=spec,
        E=E,
        nu=nu,
    )
    thd = 1e-6  # theshold
    assert (iso.G - calc_shear_modulus(E, nu)) < thd
    iso = IsoMaterial(
        name=name,
        specification=spec,
        E=E,
        G=G,
    )
    thd = 1e-6  # theshold
    assert (iso.nu - calc_poisson_ratio(E, G)) < thd


def test_iso_material_ValueError() -> None:
    """test class initialization with strings instead of numbers,
    TypeError exceptions shall occour"""
    name = "Ti-6Al-4V_ab_Annealed_Plate"
    spec = "AIMS03-18-006"
    E = 110.3e3
    G = 42.75e3
    nu = 310e-3
    with pytest.raises(TypeError):
        IsoMaterial(
            name=name,
            specification=spec,
            E="test",
            G=G,
            nu=nu,
        )
    with pytest.raises(TypeError):
        IsoMaterial(
            name=name,
            specification=spec,
            E=E,
            G="test",
            nu=nu,
        )
    with pytest.raises(TypeError):
        IsoMaterial(
            name=name,
            specification=spec,
            E=E,
            G=G,
            nu="test",
        )


def test_iso_material_TypeError() -> None:
    """test class initialization with wrong arguments,
    TypeError exceptions shall occour"""
    name = "Ti-6Al-4V_ab_Annealed_Plate"
    spec = "AIMS03-18-006"
    E = 110.3e3
    G = 42.75e3
    nu = 310e-3
    with pytest.raises(TypeError):
        IsoMaterial()
    with pytest.raises(TypeError):
        IsoMaterial(
            name=name,
        )
    with pytest.raises(TypeError):
        IsoMaterial(
            name=name,
            specification=spec,
        )
    with pytest.raises(TypeError):
        IsoMaterial(name=name, specification=spec, E=E)
    with pytest.raises(TypeError):
        IsoMaterial(
            name=name,
            specification=spec,
            G=G,
        )
    with pytest.raises(TypeError):
        IsoMaterial(
            name=name,
            specification=spec,
            nu=nu,
        )
    with pytest.raises(TypeError):
        IsoMaterial(
            name=name,
            specification=spec,
            G=G,
            nu=nu,
        )

if __name__ == "__main__":
    test_iso_material_init()
    test_iso_material_ValueError()
    test_iso_material_TypeError()
