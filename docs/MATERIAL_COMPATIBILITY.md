# Material compatibility

Compatibility is evaluated by material family, reinforcement architecture,
required properties, and model implementation. Names in the catalog do not enable
unsupported calculations.

| Model | Enabled families | Current assumptions |
|---|---|---|
| Effective elastic and CTE properties | Fibre-reinforced polymer, metal-matrix, particulate | Scalar mixture and inverse-mixture estimates |
| Uniaxial thermal response | Fibre-reinforced polymer, metal-matrix, particulate | Linear elastic free or fully restrained uniaxial response |
| Classical Laminate Theory | Fibre-reinforced polymer | Plane stress, continuous-fibre plies, supplied stacking sequence |
| Effective conductivity | None | Missing conductivity data and model |
| Transient thermal | None | Missing geometry, boundary-value solver, and verification |

Missing properties, unsupported architectures, out-of-range temperatures, and
unsupported model/family combinations must be rejected by the backend.
