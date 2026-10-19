"""Validated simulation orchestration."""

from dataclasses import asdict, dataclass
from .clt import LaminateResult, Ply, analyze_laminate
from .materials import MATERIALS, Material, ValidationError
from .models import EffectiveProperties, effective_properties, restrained_thermal_stress, thermal_strain


@dataclass(frozen=True)
class LaminateInput:
    angles_deg: tuple[float, ...]
    ply_thickness_m: float


@dataclass(frozen=True)
class SimulationInput:
    material_name: str
    fibre_volume_fraction: float
    reference_temperature_k: float
    operating_temperature_k: float
    laminate: LaminateInput | None = None
    boundary_condition: str = "Fully restrained (uniaxial estimate)"
    material_source: str = ""


@dataclass(frozen=True)
class SimulationResult:
    inputs: dict[str, object]
    effective_properties: EffectiveProperties
    delta_temperature_k: float
    thermal_strain_1: float
    restrained_stress_1_pa: float | None
    laminate: LaminateResult | None
    warnings: tuple[str, ...]


def run_simulation(config: SimulationInput) -> SimulationResult:
    if config.material_name not in MATERIALS:
        raise ValidationError(f"Unsupported material: {config.material_name}")
    material: Material = MATERIALS[config.material_name]
    material.validate_fraction(config.fibre_volume_fraction)
    material.validate_temperature(config.reference_temperature_k)
    material.validate_temperature(config.operating_temperature_k)
    if config.boundary_condition not in {"Free expansion", "Fully restrained (uniaxial estimate)"}:
        raise ValidationError(f"Unsupported boundary condition: {config.boundary_condition}")
    props = effective_properties(material, config.fibre_volume_fraction)
    dt = config.operating_temperature_k - config.reference_temperature_k
    laminate_result = None
    if config.laminate is not None:
        if "CLT" not in material.supported_models:
            raise ValidationError(
                f"{material.name} does not support the Classical Laminate Theory model."
            )
        if config.laminate.ply_thickness_m <= 0:
            raise ValidationError("Ply thickness must be positive.")
        plies = [Ply(angle, config.laminate.ply_thickness_m) for angle in config.laminate.angles_deg]
        laminate_result = analyze_laminate(props, material.poisson12, plies, dt)
    return SimulationResult(
        inputs=asdict(config), effective_properties=props, delta_temperature_k=dt,
        thermal_strain_1=thermal_strain(props.alpha1_per_k, dt),
        restrained_stress_1_pa=(
            restrained_thermal_stress(props.e1_pa, props.alpha1_per_k, dt)
            if config.boundary_condition == "Fully restrained (uniaxial estimate)"
            else None
        ),
        laminate=laminate_result,
        warnings=("Preliminary linear-elastic estimate; not a safety certification.",
                  "Reference material properties require verification for a specific supplier and temperature history."),
    )
