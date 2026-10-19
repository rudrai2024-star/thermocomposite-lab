from functools import lru_cache

from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "ThermoComposite Lab API"
    environment: str = "development"
    database_url: str | None = None
    cors_origins: str = "http://127.0.0.1:5173,http://localhost:5173"
    secret_key: str | None = None
    session_ttl_seconds: int = 3600

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    @model_validator(mode="after")
    def validate_production_configuration(self) -> "Settings":
        if self.environment.lower() == "production":
            if not self.secret_key or len(self.secret_key) < 32:
                raise ValueError("Production SECRET_KEY must be at least 32 characters.")
            if not self.database_url or not self.database_url.startswith(
                ("postgresql://", "postgresql+psycopg://")
            ):
                raise ValueError("Production DATABASE_URL must use PostgreSQL.")
            if not self.allowed_origins:
                raise ValueError("Production CORS_ORIGINS must contain an explicit origin.")
        return self

    @property
    def resolved_database_url(self) -> str:
        return self.database_url or "sqlite:///./backend/thermocomposite.db"

    @property
    def allowed_origins(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
