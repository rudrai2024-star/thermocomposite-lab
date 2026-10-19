"""Export actual simulation results without inventing unavailable values."""

import json
from dataclasses import asdict
from .simulation import SimulationResult


def result_to_dict(result: SimulationResult) -> dict[str, object]:
    data = asdict(result)
    data["metadata"] = {
        "author": "Rudrajyoti Paul",
        "units": {
            "temperature": "K",
            "temperature_difference": "K",
            "modulus": "Pa",
            "thermal_expansion": "1/K",
            "strain": "dimensionless",
            "stress": "Pa",
            "laminate_force_resultant": "N/m",
            "laminate_moment_resultant": "N",
            "curvature": "1/m",
            "ply_thickness": "m",
        },
        "material_source": result.inputs.get("material_source"),
        "model": "effective properties + thermal response + Classical Laminate Theory",
    }
    return data


def result_to_json(result: SimulationResult) -> str:
    return json.dumps(result_to_dict(result), indent=2, default=lambda value: value.tolist())
