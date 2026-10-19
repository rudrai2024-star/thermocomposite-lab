from thermo_composite.reporting import result_to_json
import pytest
from thermo_composite.materials import ValidationError
from thermo_composite.simulation import LaminateInput, SimulationInput, run_simulation


def test_end_to_end_result_and_report():
    result = run_simulation(SimulationInput(
        "Carbon fibre / epoxy", 0.6, 293.15, 353.15, LaminateInput((0, 90, 90, 0), 0.000125)
    ))
    assert result.delta_temperature_k == 60
    assert result.laminate is not None
    report = result_to_json(result)
    assert '"effective_properties"' in report
    assert '"units"' in report
    assert '"author": "Rudrajyoti Paul"' in report


def test_free_expansion_does_not_report_restrained_stress():
    result = run_simulation(SimulationInput(
        "Carbon fibre / epoxy", 0.6, 293.15, 353.15,
        boundary_condition="Free expansion",
    ))
    assert result.restrained_stress_1_pa is None


def test_unsupported_material_model_is_rejected():
    with pytest.raises(ValidationError, match="does not support"):
        run_simulation(SimulationInput(
            "Aluminium / silicon carbide", 0.4, 293.15, 353.15,
            LaminateInput((0, 90), 0.000125),
        ))
