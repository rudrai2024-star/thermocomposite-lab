# 11 — Algorithms and Data Processing

Simulation resolves a material, validates volume fraction/temperature/boundary inputs, computes effective properties and thermal output, optionally invokes CLT, returns warnings/metadata, and persists through the simulation route. Thermal curves sample the requested interval using constant material properties; comparison repeats for selected materials. Export serializes SVG/CSV/JSON beneath `Graphs/generated`; validated artifact names are used for retrieval.

Manual and synthetic testing share test-specific calculation functions. Tensile initial modulus uses a linear fit over an initial segment and fit/point checks; it is not a full standardized modulus protocol. Synthetic mode produces seeded deterministic 21-point fixtures and labels them as software-test data.

Research parsing handles supported file/source types, size and archive-path checks, checksums/provenance, and conservative numerical x/y candidates. It does not reliably digitize arbitrary paper figures and is not connected to upload/persistence. Quantity planning converts units, calculates block volume `LWH` or cylinder volume `π(d/2)²L`, mass `ρV`, and allowance multiplier `1+pct/100`; it does not optimize process yield or cost.
