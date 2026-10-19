from dataclasses import asdict, is_dataclass
from contextlib import asynccontextmanager
from typing import Any

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import desc, text
from sqlalchemy.orm import Session
from starlette.middleware.base import BaseHTTPMiddleware

from thermo_composite.materials import MATERIALS, ValidationError
from thermo_composite.simulation import LaminateInput, SimulationInput, run_simulation
from thermo_composite.taxonomy import model_compatibility, taxonomy_payload

from .core.config import get_settings
from .core.database import get_db, init_db
from .models import SimulationRecord
from .schemas import (
    HealthResponse,
    MaterialDetail,
    MaterialSummary,
    SimulationRequest,
    SimulationResponse,
)

settings = get_settings()


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        response.headers.setdefault("X-Content-Type-Options", "nosniff")
        response.headers.setdefault("X-Frame-Options", "DENY")
        response.headers.setdefault("Referrer-Policy", "no-referrer")
        response.headers.setdefault(
            "Permissions-Policy", "camera=(), microphone=(), geolocation=()"
        )
        if settings.environment.lower() == "production":
            response.headers.setdefault(
                "Strict-Transport-Security", "max-age=31536000; includeSubDomains"
            )
        return response


@asynccontextmanager
async def lifespan(_: FastAPI):
    init_db()
    yield


app = FastAPI(title=settings.app_name, version="1.0.0", lifespan=lifespan)
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=bool(settings.allowed_origins),
    allow_methods=["GET", "POST"],
    allow_headers=["Authorization", "Content-Type"],
)


def _jsonable(value: Any) -> Any:
    if is_dataclass(value):
        return _jsonable(asdict(value))
    if hasattr(value, "tolist"):
        return value.tolist()
    if isinstance(value, dict):
        return {key: _jsonable(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_jsonable(item) for item in value]
    return value


@app.get("/api/v1/health", response_model=HealthResponse)
def health(db: Session = Depends(get_db)) -> HealthResponse:
    try:
        db.execute(text("SELECT 1"))
        database = "ok"
    except Exception:
        database = "unavailable"
    return HealthResponse(status="ok", service=settings.app_name, database=database)


@app.get("/api/v1/materials", response_model=list[MaterialSummary])
def list_materials() -> list[MaterialSummary]:
    return [MaterialSummary.model_validate(material) for material in MATERIALS.values()]


@app.get("/api/v1/materials/{material_name:path}", response_model=MaterialDetail)
def get_material(material_name: str) -> MaterialDetail:
    material = MATERIALS.get(material_name)
    if material is None:
        raise HTTPException(status_code=404, detail="Material not found.")
    return MaterialDetail.model_validate(material)


@app.get("/api/v1/taxonomy")
def taxonomy() -> dict[str, list[dict[str, object]]]:
    return taxonomy_payload()


@app.get("/api/v1/compatibility/{material_family}/{model_key}")
def compatibility(material_family: str, model_key: str) -> dict[str, object]:
    return model_compatibility(material_family, model_key)


@app.post("/api/v1/simulations", response_model=SimulationResponse, status_code=201)
def simulate(request: SimulationRequest, db: Session = Depends(get_db)) -> SimulationResponse:
    config = SimulationInput(
        material_name=request.material_name,
        fibre_volume_fraction=request.fibre_volume_fraction,
        reference_temperature_k=request.reference_temperature_k,
        operating_temperature_k=request.operating_temperature_k,
        laminate=(
            LaminateInput(tuple(request.laminate.angles_deg), request.laminate.ply_thickness_m)
            if request.laminate
            else None
        ),
        boundary_condition=request.boundary_condition,
        material_source=request.material_source,
    )
    try:
        result = run_simulation(config)
    except ValidationError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    result_payload = _jsonable(result)
    record = SimulationRecord(
        material_name=request.material_name,
        request_payload=request.model_dump(mode="json"),
        result_payload=result_payload,
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return SimulationResponse(
        effective_properties=_jsonable(result.effective_properties),
        restrained_stress_1_pa=result.restrained_stress_1_pa,
        inputs=result.inputs,
        delta_temperature_k=result.delta_temperature_k,
        thermal_strain_1=result.thermal_strain_1,
        laminate=_jsonable(result.laminate),
        warnings=list(result.warnings),
        record_id=record.id,
    )


@app.get("/api/v1/simulations")
def list_simulations(db: Session = Depends(get_db)) -> list[dict[str, Any]]:
    records = db.query(SimulationRecord).order_by(
        desc(SimulationRecord.created_at), desc(SimulationRecord.id)
    ).limit(100).all()
    return [
        {
            "id": record.id,
            "material_name": record.material_name,
            "created_at": record.created_at.isoformat() if record.created_at else "",
            "request_payload": record.request_payload,
            "result_payload": record.result_payload,
        }
        for record in records
    ]
