# Scientific model registry

The current backend reuses the existing Python scientific engine. Enabled models
are declared in `thermo_composite/taxonomy.py` and are intentionally narrower
than the complete catalog.

- Effective properties: longitudinal modulus uses a direct mixture estimate;
  transverse modulus and shear modulus use inverse-mixture estimates; directional
  CTE is retained.
- Thermal response: `alpha * delta_temperature`; fully restrained uniaxial stress
  is `-E1 * alpha1 * delta_temperature`. Free expansion reports no restrained
  stress.
- Classical Laminate Theory: plane-stress transformed ply stiffness with A/B/D
  matrices, thermal resultants, mid-plane strain, curvature, and ply stress
  recovery.

These are preliminary linear-elastic estimates. They do not model damage, creep,
oxidation, moisture, transient heat transfer, or certification allowables.
