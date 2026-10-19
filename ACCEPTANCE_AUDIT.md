# ThermoComposite Lab acceptance audit

Audit date: 2026-10-18  
Scope: current source tree, automated tests, clean install, and live Streamlit workflow.  
Audit method: source inspection, numerical probes, browser interaction on the local app, and a fresh virtual environment.

## Evidence

- Baseline suite before this acceptance pass: 10 passed with the project import path.
- Final suite after fixes: **11 passed**.
- Plain `.venv/bin/pytest -q` now succeeds with the project `pytest.ini`: **11 passed**.
- `pip check`: no broken requirements.
- `py_compile`: application, package, and tests compiled successfully.
- Live browser workflow on `http://localhost:8503`: dashboard empty state, dashboard CTA navigation, thermal form, simulation execution, real metrics, laminate tables, and JSON download were exercised.
- Free-expansion browser run displayed `Not applicable` for restrained stress and retained the selected boundary condition.
- Live dashboard render visibly includes the `Rudrajyoti Paul` attribution footer.
- HTTP smoke check returned `200 OK`.

## Defect register

| ID | Severity | Finding | Evidence | Required fix | Status |
|---|---|---|---|---|---|
| A-001 | HIGH | Boundary-condition selector did not affect the calculation; free expansion still displayed a restrained stress. | `app.py` selected a boundary but always called the default model; live result showed a stress for `Free expansion`. | Pass the selected boundary into the simulation and represent non-applicable stress explicitly. | Fixed; regression test and browser evidence |
| A-002 | HIGH | Materials without CLT support could be sent through the laminate workflow. | Aluminium/silicon-carbide advertised only effective properties and thermal response, but the UI always built a laminate. | Reject unsupported CLT requests with a user-facing validation error. | Fixed; regression test |
| A-003 | HIGH | Effective transverse CTE was identical to longitudinal CTE for anisotropic fibre composites. | `models.py` used the same volume-weighted expression for `alpha1` and `alpha2`. | Use a documented directional approximation and test that anisotropic inputs remain directional. | Fixed; model documentation and regression test |
| A-004 | HIGH | Dashboard “Open Thermal Simulator” control did not navigate. | Button only wrote an unused `_jump` value. | Apply the pending navigation before the radio widget is instantiated and rerun. | Fixed; browser navigation evidence |
| A-005 | MEDIUM | Exported reports did not include explicit unit metadata or material provenance. | `reporting.py` serialized dataclasses only. | Add a metadata block with units, source, and model. | Fixed; report test |
| A-009 | HIGH | Transformed CLT stiffness was assembled upper-triangular and symmetrized, halving `Q12` and affecting laminate stiffness/results. | Independent zero-degree A-matrix benchmark failed before the fix; the corrected benchmark now passes. | Assemble all symmetric `Qbar` entries directly and retain the independent benchmark. | Fixed; `tests/test_clt.py` and direct benchmark |
| A-006 | MEDIUM | Catalogue provenance is an engineering-estimate statement, not a traceable publication or supplier citation. | Material records say “Engineering reference estimate; verify against supplier data”; no URL, document identifier, test condition, uncertainty, or measured-data status is packaged. | Add traceable, licensed citations and conditions, or keep the affected entries clearly marked as uncited estimates and restrict their use. | Incomplete; no source was fabricated |
| A-007 | MEDIUM | Hypothetical/custom combination workflow is not implemented. | Material Builder selects an existing catalogue entry; it does not accept constituent combinations or label a generated candidate as hypothetical. | Add a compatibility/data-completeness workflow before claiming support for custom combinations. | Incomplete; intentionally not added during this audit |
| A-008 | MEDIUM | Required FastAPI/typed API integration is absent. | Repository contains a Streamlit entry point and no API package, schemas, health endpoint, or API tests. | Decide and implement the separate backend/frontend architecture, then test the HTTP workflow. | Incomplete; intentionally not added during this audit |
| A-010 | HIGH | Material Builder claimed every catalogue entry was valid for CLT, including aluminium/silicon-carbide, which explicitly does not support CLT. | The success message was unconditional even when `supported_models` omitted CLT. | Report the actual supported model list in the validation message. | Fixed; source inspection and regression suite |
| A-011 | MEDIUM | Non-finite laminate angles or temperature changes could reach NumPy calculations and produce invalid results instead of a validation message. | `Ply(float("nan"), ...)` was accepted before the guard. | Reject non-finite laminate inputs before assembling ABD. | Fixed; regression test and targeted probe |
| A-012 | LOW | Reported clean-environment command depended on an implicit import path; plain `.venv/bin/pytest` failed collection. | Direct pytest executable could not import `thermo_composite`; `pytest.ini` was absent. | Declare the project import path in pytest configuration. | Fixed; plain pytest now passes |

## Acceptance checks

### Design reference match

**Pass with qualification.** The live UI uses the supplied references’ design principles:
dark charcoal background, bright lime selected states, rounded panels, navigation rail,
summary cards, data tables, and interactive Plotly output. It does not copy unrelated
financial/data-analysis content. Responsive/mobile behavior was not exhaustively tested.

### Visible controls

**Pass for implemented controls.** Navigation, material selectors, sliders, temperature
inputs, boundary selector, stacking sequence, simulation button, search, family filter,
comparison selectors, and report download were inspected. Dashboard CTA navigation was
fixed and verified. Decorative quick-action cards are not controls and are not labeled as
buttons.

### Numerical provenance

**Pass after fixes.** Summary values, tables, and plots are derived from `run_simulation`.
Reports now include explicit units and the selected material source field. The catalogue
source field remains an estimate warning rather than a fabricated citation.

### Thermal stress

**Pass after fixes for the supported scalar model.** Restrained stress is only calculated
for `Fully restrained (uniaxial estimate)`. Free expansion returns an explicit
non-applicable value, while CLT remains a separate laminate response.

### Classical Laminate Theory

**Verified for current scope.** The suite checks symmetric-laminate B-coupling behavior,
an independently constructed zero-degree A matrix, free single-ply thermal stress
recovery, invalid laminate rejection, and end-to-end serialization. This is numerical
software verification, not experimental validation.

### API and clean environment

**API incomplete.** No API exists to test.  
**Clean environment pass with local-environment qualification.** The pinned environment
is present, the app serves HTTP 200, and plain `.venv/bin/pytest -q` runs 11 tests
successfully. A network request for Streamlit's optional Segment analytics script was
refused by the local browser environment; it did not prevent the app from rendering or
running the local workflow.

## Remaining release blockers

1. Add traceable material citations and property conditions, or restrict the catalogue to
   documented user-supplied/reference records.
2. Decide whether the separate FastAPI/React architecture is a required next phase.
3. Implement and test hypothetical/custom material compatibility only when property
   completeness and model applicability can be enforced.
4. Add responsive/mobile browser coverage before claiming full UI acceptance.
