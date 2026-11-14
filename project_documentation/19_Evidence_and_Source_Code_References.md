# 19 — Evidence and Source Code References

Paths are repository-relative; source is authoritative over labels and older prose.

| Subject | Evidence |
|---|---|
| UI routes | `frontend/src/App.tsx` |
| API client/origin | `frontend/src/api/client.ts`, `api-url.mjs`, `frontend/tests/api-url.test.mjs` |
| Vite/build/hosting | `frontend/vite.config.ts`, `frontend/package.json`, `netlify.toml` |
| Testing UI | `frontend/src/components/TestingLaboratory.tsx` |
| Thermal UI/charts | `frontend/src/components/ThermalAnalysis.tsx`, `ThermalCharts.tsx` |
| Quantity UI | `frontend/src/components/MaterialQuantityPlanner.tsx` |
| Backend app/routes | `backend/main.py` and route modules under `backend/` |
| Testing formulas/fixtures | `backend/composite_testing/calculations.py`, `synthetic.py` |
| Research query/parser | `backend/composite_testing/research.py`, `research_store.py`, `ingestion.py` |
| Quantity equations | `backend/material_quantity/calculations.py` |
| Curves and export | `backend/thermal_analysis.py` |
| Materials/equations/simulation | `thermo_composite/materials.py`, `models.py`, `simulation.py` |
| CLT/taxonomy/reporting | `thermo_composite/clt.py`, `taxonomy.py`, `reporting.py` |
| Persistence | `backend/**/models.py`, `backend/migrations/versions/` |
| Tests/legacy UI | `tests/`, `backend/tests/`, `app.py` |
| Research archive | `research_data/` and relational research records |

A route existing does not prove a connected UI workflow; both were checked. A parser is not an upload product. Source/archive counts are not observation counts. Synthetic fixtures are not experimental evidence. Automated tests are not physical validation.
