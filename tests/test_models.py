import pytest
from thermo_composite.materials import MATERIALS, ValidationError
from thermo_composite.models import effective_properties, restrained_thermal_stress, thermal_strain


def test_rule_of_mixtures_and_limits():
    material = MATERIALS["Carbon fibre / epoxy"]
    props = effective_properties(material, 0.0)
    assert props.e1_pa == pytest.approx(material.matrix_modulus_pa)
    assert effective_properties(material, 1.0).e1_pa == pytest.approx(material.fibre_modulus_pa)
    anisotropic = effective_properties(material, 0.55)
    assert anisotropic.alpha2_per_k != pytest.approx(anisotropic.alpha1_per_k)


def test_invalid_fraction_and_temperature_rejected():
    material = MATERIALS["Glass fibre / epoxy"]
    with pytest.raises(ValidationError):
        effective_properties(material, 1.1)
    with pytest.raises(ValidationError):
        material.validate_temperature(100.0)


def test_thermal_equations_are_linear_and_signed():
    assert thermal_strain(10e-6, 50) == pytest.approx(5e-4)
    assert restrained_thermal_stress(100e9, 10e-6, 50) == pytest.approx(-50e6)
