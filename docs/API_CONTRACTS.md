# API contracts

Existing endpoints remain unchanged:

- `GET /api/v1/health`
- `GET /api/v1/materials`
- `GET /api/v1/materials/{material_name}`
- `GET /api/v1/simulations`
- `POST /api/v1/simulations`

The taxonomy metadata endpoints are:

- `GET /api/v1/taxonomy`
- `GET /api/v1/compatibility/{material_family}/{model_key}`

Compatibility responses explicitly include `compatible` and a reason. A
catalog-only family therefore cannot be mistaken for an enabled calculation.
