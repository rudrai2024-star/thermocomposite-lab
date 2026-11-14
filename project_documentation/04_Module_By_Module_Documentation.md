# 04 — Module-by-Module Documentation

| Area | Main files | Execution path and status |
|---|---|---|
| Dashboard/navigation | `frontend/src/App.tsx` | Main route composition; not an independent solver. |
| Materials explorer | `App.tsx`, `MaterialVisualizer.tsx` | Lists/filters material data; SVG is illustrative, not a micrograph. API scope is narrower than core records. |
| Material builder | `App.tsx` | Configuration/validation UI; no authoring persistence. Partial. |
| Thermal simulation | `thermo_composite/simulation.py`, routes | Validates and calculates; persists runs. Implemented, tests pass; simplified model. |
| Thermal analysis | `ThermalAnalysis.tsx`, `ThermalCharts.tsx`, `backend/thermal_analysis.py` | Curve/compare/export paths. Export test not run in audit. |
| Laminate | `thermo_composite/clt.py`, `LaminateStackViewer.tsx` | CLT calculation and stack visualization; no failure/damage analysis. |
| Composite testing | `TestingLaboratory.tsx`, `backend/composite_testing/` | Research/manual/synthetic modes. Manual and synthetic support nine destructive tests; 18 research categories; no NDT engine. |
| Quantity planner | `MaterialQuantityPlanner.tsx`, `backend/material_quantity/` | Conversion, volume/mass and usage records; tests pass. |
| Compare/reports | `App.tsx` | Lists saved runs; report bundle/export is not wired in React. |
| Methodology/settings/about | `App.tsx` | Informational, health, and local display; settings do not persist server config. |
| Login/register | `App.tsx`, `backend/auth.py` | Placeholder UI; helpers exist but no connected auth API. |
| Legacy UI | `app.py` | Separate Streamlit UI, session-state based; secondary/deprecated path. |

Backend routes in `backend/main.py` call Pydantic schemas and domain modules. The core modules are `materials.py` (reference records), `models.py` (mixture/thermal formulas), `simulation.py` (orchestration), `clt.py` (laminates), `taxonomy.py` (compatibility), and `reporting.py` (JSON serialization). Research query/store and parser are separate code paths. `backend/material_quantity/calculations.py` computes quantities; `backend/thermal_analysis.py` creates curves and artifacts.
