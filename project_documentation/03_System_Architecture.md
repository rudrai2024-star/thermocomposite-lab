# 03 — System Architecture

```mermaid
flowchart LR
  U[User] --> UI[React / TypeScript SPA]
  UI -->|/api/v1 JSON| API[FastAPI]
  API --> R[Routes and Pydantic schemas]
  R --> C[thermo_composite scientific core]
  R --> T[Testing and research services]
  R --> Q[Quantity calculations]
  R --> ORM[SQLAlchemy]
  ORM --> DB[(SQLite database)]
  API --> X[Graphs/generated exports]
  S[Legacy Streamlit app.py] --> C
```

The primary frontend calls FastAPI. In development Vite proxies `/api/v1` to the local backend. FastAPI validates requests, dispatches route services and persists simulations, usage transactions, and research records through SQLAlchemy. Domain code is separated into scientific, testing, quantity, and thermal-analysis modules. Thermal export writes SVG/CSV/JSON artifacts. Streamlit remains a separate legacy caller of the scientific core.

```mermaid
sequenceDiagram
 actor User
 participant UI as React UI
 participant API as FastAPI
 participant S as Domain service
 participant DB as SQL
 User->>UI: Submit inputs
 UI->>API: JSON request
 API->>API: Validate schema
 API->>S: Calculate or query
 S-->>API: Result
 API->>DB: Persist if route requires
 API-->>UI: JSON response
 UI-->>User: Render result
```

The research parser is not connected to an upload/persistence API. Auth helpers are not middleware. There is no background job queue. See [API](10_API_Documentation.md) and [module status](04_Module_By_Module_Documentation.md).
