"""Material data and validation."""

from dataclasses import dataclass


class ValidationError(ValueError):
    """Raised when an input is physically unsupported."""


@dataclass(frozen=True)
class Material:
    name: str
    fibre_modulus_pa: float
    matrix_modulus_pa: float
    fibre_alpha_per_k: float
    matrix_alpha_per_k: float
    poisson12: float
    fibre_shear_modulus_pa: float
    matrix_shear_modulus_pa: float
    density_kg_m3: float
    source: str
    valid_temperature_range_k: tuple[float, float] = (233.15, 423.15)
    family: str = "Fibre-reinforced polymer"
    reinforcement: str = "Continuous fibre"
    matrix: str = "Polymer"
    form: str = "Unidirectional"
    status: str = "Reference estimate"
    supported_models: tuple[str, ...] = ("effective properties", "thermal response", "CLT")

    def validate_fraction(self, fibre_volume_fraction: float) -> None:
        if not 0.0 <= fibre_volume_fraction <= 1.0:
            raise ValidationError("Fibre volume fraction must be between 0 and 1.")

    def validate_temperature(self, temperature_k: float) -> None:
        lo, hi = self.valid_temperature_range_k
        if not lo <= temperature_k <= hi:
            raise ValidationError(
                f"Temperature {temperature_k:.2f} K is outside the supported "
                f"range [{lo:.2f}, {hi:.2f}] K for {self.name}."
            )


MATERIALS = {
    "Carbon fibre / epoxy": Material(
        "Carbon fibre / epoxy", 230e9, 3.5e9, -0.2e-6, 55e-6, 0.30,
        15e9, 1.3e9, 1550, "Engineering reference estimate; verify against supplier data."
    ),
    "Glass fibre / epoxy": Material(
        "Glass fibre / epoxy", 72e9, 3.5e9, 5e-6, 55e-6, 0.27,
        30e9, 1.3e9, 2000, "Engineering reference estimate; verify against supplier data."
    ),
    "Aramid fibre / epoxy": Material(
        "Aramid fibre / epoxy", 130e9, 3.5e9, -2.0e-6, 55e-6, 0.34,
        5.5e9, 1.3e9, 1380, "Engineering reference estimate; verify against supplier data.",
        family="Fibre-reinforced polymer", reinforcement="Aramid fibre", matrix="Epoxy",
        status="Reference estimate",
    ),
    "Basalt fibre / epoxy": Material(
        "Basalt fibre / epoxy", 89e9, 3.5e9, 8.0e-6, 55e-6, 0.28,
        36e9, 1.3e9, 2050, "Engineering reference estimate; verify against supplier data.",
        family="Fibre-reinforced polymer", reinforcement="Basalt fibre", matrix="Epoxy",
        status="Reference estimate",
    ),
    "Carbon fibre / PEEK": Material(
        "Carbon fibre / PEEK", 230e9, 3.6e9, -0.2e-6, 45e-6, 0.30,
        15e9, 1.4e9, 1510, "Engineering reference estimate; verify against supplier data.",
        valid_temperature_range_k=(233.15, 573.15), matrix="PEEK",
        status="Reference estimate",
    ),
    "Aluminium / silicon carbide": Material(
        "Aluminium / silicon carbide", 420e9, 69e9, 4.0e-6, 23e-6, 0.29,
        170e9, 26e9, 3000, "Engineering reference estimate; verify constituent and process data.",
        family="Metal-matrix composite", reinforcement="Silicon carbide particle",
        matrix="Aluminium", form="Particulate", status="Reference estimate",
        supported_models=("effective properties", "thermal response"),
    ),
}
