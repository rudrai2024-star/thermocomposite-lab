"""Explicit material taxonomy and model compatibility metadata.

Catalog entries may describe a material family without enabling a calculation.
Only records with complete properties and an explicitly supported model are
accepted by the scientific service.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class MaterialFamily:
    key: str
    label: str
    material_type: str
    implemented: bool
    note: str


@dataclass(frozen=True)
class ReinforcementArchitecture:
    key: str
    label: str
    required_parameters: tuple[str, ...]
    supported_models: tuple[str, ...]
    implemented: bool


@dataclass(frozen=True)
class ScientificModel:
    key: str
    label: str
    required_properties: tuple[str, ...]
    supported_families: tuple[str, ...]
    implemented: bool
    assumptions: str


MATERIAL_FAMILIES = (
    MaterialFamily("fibre_reinforced_polymer", "Fibre-reinforced polymer", "composite", True, "Supported for registered systems with complete scalar properties."),
    MaterialFamily("metal_matrix", "Metal-matrix composite", "composite", True, "Only registered effective-property systems are enabled; CLT is not enabled."),
    MaterialFamily("ceramic_matrix", "Ceramic-matrix composite", "composite", False, "Catalog category only; dedicated high-temperature models are not implemented."),
    MaterialFamily("carbon_carbon", "Carbon-carbon", "composite", False, "Catalog category only; oxidation and temperature-dependent data are required."),
    MaterialFamily("hybrid", "Hybrid composite", "composite", False, "Requires ply- or phase-specific homogenization not implemented in the current engine."),
    MaterialFamily("particle_reinforced", "Particle-reinforced composite", "composite", True, "Registered particulate systems use effective properties only."),
    MaterialFamily("nanocomposite", "Nanocomposite", "composite", False, "Catalog category only; nanoscale models and data are not implemented."),
    MaterialFamily("structural", "Structural composite", "configuration", False, "Sandwich, woven, braided, and 3D architectures require dedicated models."),
)

ARCHITECTURES = (
    ReinforcementArchitecture("continuous_unidirectional", "Continuous unidirectional", ("fibre_volume_fraction",), ("effective_properties", "thermal_response", "clt"), True),
    ReinforcementArchitecture("particulate", "Particulate reinforcement", ("particle_volume_fraction",), ("effective_properties", "thermal_response"), True),
    ReinforcementArchitecture("woven_plain", "Plain-weave fabric", ("areal_weight",), ("clt",), False),
    ReinforcementArchitecture("woven_twill", "Twill-weave fabric", ("areal_weight",), ("clt",), False),
    ReinforcementArchitecture("hybrid", "Hybrid reinforcement", ("constituents",), (), False),
    ReinforcementArchitecture("sandwich", "Sandwich or honeycomb", ("core_thickness",), (), False),
    ReinforcementArchitecture("random_short", "Random or chopped fibre", ("fibre_length",), (), False),
)

MODELS = (
    ScientificModel("effective_properties", "Effective elastic and CTE properties", ("fibre_modulus_pa", "matrix_modulus_pa", "fibre_alpha_per_k", "matrix_alpha_per_k"), ("fibre_reinforced_polymer", "metal_matrix", "particle_reinforced"), True, "Scalar rule-of-mixtures and inverse-rule estimates; not a universal homogenization model."),
    ScientificModel("thermal_response", "Uniaxial thermal response", ("e1_pa", "alpha1_per_k"), ("fibre_reinforced_polymer", "metal_matrix", "particle_reinforced"), True, "Linear elastic, fully restrained uniaxial estimate or free expansion."),
    ScientificModel("clt", "Classical Laminate Theory", ("e1_pa", "e2_pa", "g12_pa", "poisson12"), ("fibre_reinforced_polymer",), True, "Plane-stress continuous-fibre laminate with supported stacking sequences."),
    ScientificModel("effective_conductivity", "Effective thermal conductivity", ("thermal_conductivity",), (), False, "No conductivity data or implemented model is currently available."),
    ScientificModel("transient_thermal", "Transient heat transfer", ("thermal_conductivity", "specific_heat", "density", "geometry"), (), False, "Requires geometry, boundary conditions, initial conditions, and a verified numerical solver."),
)


def taxonomy_payload() -> dict[str, list[dict[str, object]]]:
    return {
        "families": [item.__dict__ for item in MATERIAL_FAMILIES],
        "architectures": [item.__dict__ for item in ARCHITECTURES],
        "models": [item.__dict__ for item in MODELS],
    }


def model_compatibility(material_family: str, model_key: str) -> dict[str, object]:
    model = next((item for item in MODELS if item.key == model_key), None)
    if model is None:
        return {"compatible": False, "reason": f"Unknown scientific model: {model_key}."}
    compatible = model.implemented and material_family in model.supported_families
    if compatible:
        return {"compatible": True, "reason": "Material family and model are supported.", "model": model.__dict__}
    return {
        "compatible": False,
        "reason": f"{model.label} is not implemented for the {material_family} family.",
        "model": model.__dict__,
    }
