"""Scalar composite-property and thermal-response equations."""

from dataclasses import dataclass
from .materials import Material


@dataclass(frozen=True)
class EffectiveProperties:
    e1_pa: float
    e2_pa: float
    g12_pa: float
    alpha1_per_k: float
    alpha2_per_k: float


def effective_properties(material: Material, vf: float) -> EffectiveProperties:
    material.validate_fraction(vf)
    vm = 1.0 - vf
    e1 = vf * material.fibre_modulus_pa + vm * material.matrix_modulus_pa
    e2 = 1.0 / (vf / material.fibre_modulus_pa + vm / material.matrix_modulus_pa)
    g12 = 1.0 / (vf / material.fibre_shear_modulus_pa + vm / material.matrix_shear_modulus_pa)
    alpha1 = vf * material.fibre_alpha_per_k + vm * material.matrix_alpha_per_k
    # Compliance-weighted transverse estimate; it is deliberately distinct
    # from the longitudinal rule and remains an approximation.
    alpha2 = (
        vf * material.fibre_alpha_per_k / material.fibre_modulus_pa
        + vm * material.matrix_alpha_per_k / material.matrix_modulus_pa
    ) / (vf / material.fibre_modulus_pa + vm / material.matrix_modulus_pa)
    return EffectiveProperties(e1, e2, g12, alpha1, alpha2)


def thermal_strain(alpha_per_k: float, delta_temperature_k: float) -> float:
    return alpha_per_k * delta_temperature_k


def restrained_thermal_stress(
    modulus_pa: float, alpha_per_k: float, delta_temperature_k: float
) -> float:
    """Reaction stress for full uniaxial restraint; compression is negative."""
    return -modulus_pa * alpha_per_k * delta_temperature_k
