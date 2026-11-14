# 06 — Classical Laminate Theory

`thermo_composite/clt.py` implements linear elastic plane-stress CLT using NumPy. It constructs reduced lamina stiffness `Q` from `E1`, `E2`, `G12`, and `ν12`, transforms stiffness for each ply orientation, and integrates across interface coordinates `zk`.

`A=Σ Q̄k(zk−zk−1)`; `B=½Σ Q̄k(zk²−zk−1²)`; `D=⅓Σ Q̄k(zk³−zk−1³)`. Together they form the ABD system relating mid-plane strain `ε0` and curvature `κ` to force/moment resultants. Thermal resultants integrate transformed stiffness and thermal expansion over the temperature change. Ply surface stress recovery uses `σ̄(z)=Q̄k[ε0+zκ−ᾱkΔT]`.

The model assumes homogeneous orthotropic plies, linear elasticity, small deformation, plane stress, perfect bonding, and classical kinematics. It does not model progressive damage, delamination, free-edge effects, viscoelasticity, cure residual stress, failure criteria, buckling, or FEM. Numerical tests exist, but this audit establishes no independent experimental benchmark. Evidence: `thermo_composite/clt.py`, `tests/test_clt.py`, and `tests/test_simulation.py`.
