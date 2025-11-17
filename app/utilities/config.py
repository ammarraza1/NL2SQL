from __future__ import annotations
from functools import lru_cache
from pathlib import Path
from pydantic import Field, AliasChoices
from pydantic_settings import BaseSettings, SettingsConfigDict

# Compute project root: .../app/utilities/config.py -> parents[2] = project_root
PROJECT_ROOT = Path(__file__).resolve().parents[2]
ENV_FILE = PROJECT_ROOT / ".env"

class Settings(BaseSettings):
    # ---- Azure OpenAI ----
    azure_openai_endpoint: str = Field(validation_alias=AliasChoices("AZURE_OPENAI_ENDPOINT"))
    azure_openai_api_key: str = Field(validation_alias=AliasChoices("AZURE_OPENAI_API_KEY"))
    azure_openai_api_version: str = Field(validation_alias=AliasChoices("AZURE_OPENAI_API_VERSION"))
    azure_openai_deployment: str = Field(validation_alias=AliasChoices("AZURE_OPENAI_DEPLOYMENT"))

    # ---- Postgres ----
    pg_host: str = Field(default="localhost", validation_alias=AliasChoices("PGHOST"))
    pg_port: int = Field(default=5432, validation_alias=AliasChoices("PGPORT"))
    pg_user: str = Field(default="postgres", validation_alias=AliasChoices("PGUSER"))
    pg_password: str = Field(default="postgres", validation_alias=AliasChoices("PGPASSWORD"))
    pg_database: str = Field(default="postgres", validation_alias=AliasChoices("PGDATABASE"))

    # ---- App ----
    app_log_level: str = Field(default="INFO", validation_alias=AliasChoices("APP_LOG_LEVEL"))
    default_row_limit: int = Field(default=200, validation_alias=AliasChoices("DEFAULT_ROW_LIMIT"))

    model_config = SettingsConfigDict(
        env_file=str(ENV_FILE),   # <— absolute path to your project .env
        case_sensitive=True,
        extra="ignore",
    )

@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
