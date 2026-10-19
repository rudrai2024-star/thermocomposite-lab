from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class HealthResponse(BaseModel):
    status: str
    service: str
    database: str


class MaterialSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    family: str
    reinforcement: str
    matrix: str
    form: str
    status: str
    valid_temperature_range_k: tuple[float, float]
    supported_models: tuple[str, ...]


class MaterialDetail(MaterialSummary):
    model_config = ConfigDict(from_attributes=True)

    fibre_modulus_pa: float
    matrix_modulus_pa: float
    fibre_alpha_per_k: float
    matrix_alpha_per_k: float
    poisson12: float
    fibre_shear_modulus_pa: float
    matrix_shear_modulus_pa: float
    density_kg_m3: float
    source: str


class LaminateRequest(BaseModel):
    angles_deg: list[float] = Field(min_length=1, max_length=100)
    ply_thickness_m: float = Field(gt=0)


class SimulationRequest(BaseModel):
    material_name: str
    fibre_volume_fraction: float = Field(ge=0, le=1)
    reference_temperature_k: float
    operating_temperature_k: float
    laminate: LaminateRequest | None = None
    boundary_condition: str = "Fully restrained (uniaxial estimate)"
    material_source: str = ""


class SimulationResponse(BaseModel):
    inputs: dict[str, Any]
    effective_properties: dict[str, float]
    delta_temperature_k: float
    thermal_strain_1: float
    restrained_stress_1_pa: float | None
    laminate: dict[str, Any] | None
    warnings: list[str]
    record_id: int
