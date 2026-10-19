# Architecture

`thermo_composite/materials.py` contains immutable material records and input
validation. `thermo_composite/models.py` contains scalar effective-property,
thermal strain, and restrained-stress equations. `thermo_composite/clt.py`
contains the plane-stress Classical Laminate Theory implementation.
`thermo_composite/simulation.py` validates and orchestrates calculations.
`thermo_composite/reporting.py` serializes actual simulation outputs.
`app.py` is the Streamlit adapter and contains no engineering equations.

All calculations use SI units internally: Pa, m, K, and N/m. UI labels convert
these values for readability. Errors are raised as `ValidationError` or
`NumericalError`; no numerical fallback is returned after a failed solve.
