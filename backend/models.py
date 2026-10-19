from datetime import datetime

from sqlalchemy import DateTime, Integer, JSON, String, func
from sqlalchemy.orm import Mapped, mapped_column

from .core.database import Base


class SimulationRecord(Base):
    __tablename__ = "simulation_records"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    material_name: Mapped[str] = mapped_column(String(160), index=True)
    request_payload: Mapped[dict] = mapped_column(JSON)
    result_payload: Mapped[dict] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
