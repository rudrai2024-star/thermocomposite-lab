import numpy as np
import pytest
from thermo_composite.clt import Ply, analyze_laminate
from thermo_composite.materials import MATERIALS, ValidationError
from thermo_composite.models import effective_properties


def test_symmetric_cross_ply_has_zero_b_matrix():
    material = MATERIALS["Glass fibre / epoxy"]
    result = analyze_laminate(effective_properties(material, 0.55), material.poisson12,
                              [Ply(0, 0.001), Ply(90, 0.001), Ply(90, 0.001), Ply(0, 0.001)], 0)
    assert np.allclose(result.b_matrix, 0, atol=1e-8)
    assert np.allclose(result.a_matrix, result.a_matrix.T)


def test_zero_degree_a_matrix_matches_independent_plane_stress_reference():
    material = MATERIALS["Carbon fibre / epoxy"]
    props = effective_properties(material, 0.55)
    nu = material.poisson12
    denominator = 1 - nu**2 * props.e2_pa / props.e1_pa
    q11 = props.e1_pa / denominator
    q22 = props.e2_pa / denominator
    q12 = nu * props.e2_pa / denominator
    expected = np.array([[q11, q12, 0], [q12, q22, 0], [0, 0, props.g12_pa]]) * 0.001
    result = analyze_laminate(props, nu, [Ply(0, 0.001)], 0)
    assert np.allclose(result.a_matrix, expected, rtol=1e-12, atol=1e-6)


def test_invalid_laminate_is_reported():
    material = MATERIALS["Carbon fibre / epoxy"]
    with pytest.raises(ValidationError):
        analyze_laminate(effective_properties(material, 0.5), material.poisson12,
                         [], 0)


def test_nonfinite_laminate_inputs_are_reported():
    material = MATERIALS["Carbon fibre / epoxy"]
    with pytest.raises(ValidationError, match="finite"):
        analyze_laminate(effective_properties(material, 0.5), material.poisson12,
                         [Ply(float("nan"), 0.001)], 0)


def test_uniform_temperature_free_laminate_has_no_recovered_stress():
    material = MATERIALS["Glass fibre / epoxy"]
    result = analyze_laminate(
        effective_properties(material, 0.55), material.poisson12,
        [Ply(0, 0.001)], 50,
    )
    stresses = np.concatenate([item["stress_pa"] for item in result.ply_stresses])
    assert np.max(np.abs(stresses)) < 1e-4
