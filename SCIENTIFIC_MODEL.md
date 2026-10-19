# Scientific model and assumptions

## Scalar model

For fibre volume fraction `Vf`, longitudinal modulus is
`E1 = Vf Ef + (1 - Vf) Em`. The transverse modulus uses the reciprocal
mixture rule `1/E2 = Vf/Ef + (1 - Vf)/Em`. Longitudinal CTE uses a
volume-weighted estimate; transverse CTE uses a compliance-weighted estimate
and is explicitly approximate. Thermal strain is
`epsilon = alpha * (T - T_ref)`. A fully restrained uniaxial estimate is
`sigma = -E * alpha * (T - T_ref)`, with sign indicating the reaction stress.

## Classical Laminate Theory

Each orthotropic ply uses reduced plane-stress stiffness `Q`, transformed to
the laminate axes as `Qbar`. Through-thickness integration gives A, B, and D.
The laminate response solves:

`[A B; B D] [epsilon0; kappa] = [N; M] + [Nth; Mth]`

where the thermal resultants are integrated from `Qbar * alphabar * dT`.
Ply stresses are recovered at the requested top and bottom surfaces using
`sigma = Qbar * (epsilon0 + z*kappa - alphabar*dT)`.

The implementation assumes linear elasticity, small strain, perfect bonding,
plane stress, uniform temperature change through the laminate, and no failure
or damage evolution. The sign convention is x/y in laminate axes, positive z
through thickness, and engineering shear strain/stress components.
