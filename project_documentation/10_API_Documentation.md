# 10 — API Documentation

Prefix: `/api/v1`. See generated OpenAPI for exact field types and constraints. Strict request models reject unexpected fields where configured.

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/health` | Health status |
| GET | `/materials` | Active material listing |
| GET | `/materials/{material_name:path}` | Material detail |
| GET | `/taxonomy` | Taxonomy catalog |
| GET | `/compatibility/{material_family}/{model_key}` | Model compatibility |
| GET | `/testing/tests` | Testing metadata |
| GET | `/testing/research/{test}` | Test-specific research query; filters include material, geometry, orientation, temperature, fractions, pagination/sort |
| POST | `/testing/calculate` | Manual testing metrics |
| POST | `/testing/synthetic` | Seeded software fixture |
| POST | `/material-quantity/calculate` | Quantity calculation |
| POST/GET | `/material-quantity/usage` | Create/list usage records |
| POST/GET | `/simulations` | Calculate/persist and list latest simulations (up to 100) |
| POST | `/thermal-curves` | Single analytical curve |
| POST | `/thermal-analysis/compare` | Compare curves |
| POST | `/thermal-analysis/export` | Write SVG/CSV/JSON artifacts |
| GET | `/thermal-analysis/artifacts/{filename}` | Download generated artifact |

No material CRUD, auth/user, research upload, dedicated CLT, simulation-by-ID, or NDT signal-analysis route was found. CLT runs through simulation. Auth helper code is not a protected API. See `backend/main.py` and route modules.
