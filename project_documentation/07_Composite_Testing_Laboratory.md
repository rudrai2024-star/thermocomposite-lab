# 07 — Composite Testing Laboratory

Three UI modes exist: research search, manual experimental values, and synthetic software-test data. Manual mode calculates from values supplied by the user; the system does not prove those values were measured correctly. Seeded synthetic data are reproducible fixtures, not experimental evidence. Research queries stored datasets; current observations are zero, so no experimental response curve is available.

| Destructive test | Implemented metric |
|---|---|
| Tensile | `σ=F/A0`, `ε=ΔL/L0`; initial linear fit with minimum-point/fit checks |
| Flexural (3-point) | `σf=3FL/(2bd²)`, `εf=6Dd/L²` |
| Compression | `σc=F/A0`, `εc=shortening/gauge`; positive magnitudes |
| Shear | `τavg=F/A` |
| Impact | `Eabs=Einitial−Eresidual` |
| Fatigue | `R=σmin/σmax`, `σa=(σmax−σmin)/2`, `σm=(σmax+σmin)/2`; no life inference |
| Creep | `ε(t)=ΔL(t)/L0`; no rate model |
| Pull-out | `τapp=Fmax/(πdLe)` |
| Short-beam ILSS | `0.75Pmax/(bh)` |

Eight NDT categories are searchable procedure metadata (including ultrasound, radiography, thermography, acoustic emission, shearography, eddy-current, visual, and penetrant groupings); there is no NDT signal-processing engine or graphable dataset. No acoustic signal should be invented.

These are basic calculations, not universal standards-conformance implementations. Preserve test-specific source, geometry, and units. Original experimental values must remain distinct from derived values. Do not rescale/stretch a curve to match different specimen dimensions; document any scientifically justified recalculation and its assumptions.
