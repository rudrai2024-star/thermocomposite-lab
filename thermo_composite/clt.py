"""Plane-stress Classical Laminate Theory."""

from dataclasses import dataclass
import numpy as np
from numpy.typing import NDArray
from .materials import ValidationError
from .models import EffectiveProperties

Array = NDArray[np.float64]


class NumericalError(RuntimeError):
    """Raised when a laminate cannot be solved reliably."""


@dataclass(frozen=True)
class Ply:
    angle_deg: float
    thickness_m: float


@dataclass(frozen=True)
class LaminateResult:
    a_matrix: Array
    b_matrix: Array
    d_matrix: Array
    midplane_strain: Array
    curvature: Array
    thermal_force: Array
    thermal_moment: Array
    ply_stresses: list[dict[str, object]]


def _q_matrix(props: EffectiveProperties, nu12: float) -> Array:
    if not 0 < nu12 < 0.5:
        raise ValidationError("Poisson ratio must be between 0 and 0.5.")
    denom = 1.0 - nu12 * nu12 * props.e2_pa / props.e1_pa
    q11 = props.e1_pa / denom
    q22 = props.e2_pa / denom
    q12 = nu12 * props.e2_pa / denom
    return np.array([[q11, q12, 0], [q12, q22, 0], [0, 0, props.g12_pa]])


def _transformed_q(q: Array, angle_deg: float) -> Array:
    m, n = np.cos(np.deg2rad(angle_deg)), np.sin(np.deg2rad(angle_deg))
    q11, q12, q22, q66 = q[0, 0], q[0, 1], q[1, 1], q[2, 2]
    qbar11 = q11*m**4 + 2*(q12+2*q66)*m*m*n*n + q22*n**4
    qbar22 = q11*n**4 + 2*(q12+2*q66)*m*m*n*n + q22*m**4
    qbar12 = (q11+q22-4*q66)*m*m*n*n + q12*(m**4+n**4)
    qbar16 = (q11-q12-2*q66)*m**3*n - (q22-q12-2*q66)*m*n**3
    qbar26 = (q11-q12-2*q66)*m*n**3 - (q22-q12-2*q66)*m**3*n
    qbar66 = (q11+q22-2*q12-2*q66)*m*m*n*n + q66*(m**4+n**4)
    return np.array([
        [qbar11, qbar12, qbar16],
        [qbar12, qbar22, qbar26],
        [qbar16, qbar26, qbar66],
    ])


def _symmetrize(matrix: Array) -> Array:
    return 0.5 * (matrix + matrix.T)


def _alpha_bar(props: EffectiveProperties, angle_deg: float) -> Array:
    m, n = np.cos(np.deg2rad(angle_deg)), np.sin(np.deg2rad(angle_deg))
    a1, a2 = props.alpha1_per_k, props.alpha2_per_k
    return np.array([(a1*m*m + a2*n*n), (a1*n*n + a2*m*m), 2*(a1-a2)*m*n])


def analyze_laminate(
    props: EffectiveProperties,
    poisson12: float,
    plies: list[Ply],
    delta_temperature_k: float,
    applied_force_n_per_m: Array | None = None,
    applied_moment_n: Array | None = None,
) -> LaminateResult:
    if not plies or any(p.thickness_m <= 0 for p in plies):
        raise ValidationError("Laminate must contain plies with positive thickness.")
    if any(not np.isfinite(p.angle_deg) or not np.isfinite(p.thickness_m) for p in plies):
        raise ValidationError("Laminate angles and thicknesses must be finite numbers.")
    if not np.isfinite(delta_temperature_k):
        raise ValidationError("Temperature change must be a finite number.")
    q = _q_matrix(props, poisson12)
    z = np.linspace(-sum(p.thickness_m for p in plies) / 2,
                    sum(p.thickness_m for p in plies) / 2, len(plies) + 1)
    a = np.zeros((3, 3)); b = np.zeros((3, 3)); d = np.zeros((3, 3))
    nth = np.zeros(3); mth = np.zeros(3)
    transformed = []
    alphas = []
    for i, ply in enumerate(plies):
        qbar = _symmetrize(_transformed_q(q, ply.angle_deg))
        alpha = _alpha_bar(props, ply.angle_deg)
        dz, dz2, dz3 = z[i+1]-z[i], z[i+1]**2-z[i]**2, z[i+1]**3-z[i]**3
        a += qbar * dz; b += 0.5*qbar*dz2; d += (1/3)*qbar*dz3
        thermal_resultant = qbar @ alpha * delta_temperature_k
        nth += thermal_resultant * dz; mth += 0.5 * thermal_resultant * dz2
        transformed.append(qbar); alphas.append(alpha)
    abd = np.block([[a, b], [b, d]])
    loads = np.concatenate((applied_force_n_per_m if applied_force_n_per_m is not None else np.zeros(3),
                            applied_moment_n if applied_moment_n is not None else np.zeros(3)))
    try:
        response = np.linalg.solve(abd, loads + np.concatenate((nth, mth)))
    except np.linalg.LinAlgError as exc:
        raise NumericalError("Laminate ABD matrix is singular; check ply inputs.") from exc
    ply_stresses = []
    for i, ply in enumerate(plies):
        for surface, zi in (("bottom", z[i]), ("top", z[i+1])):
            strain = response[:3] + zi * response[3:] - alphas[i] * delta_temperature_k
            ply_stresses.append({"ply": i + 1, "angle_deg": ply.angle_deg,
                                 "surface": surface, "z_m": zi,
                                 "stress_pa": transformed[i] @ strain})
    return LaminateResult(a, b, d, response[:3], response[3:], nth, mth, ply_stresses)
