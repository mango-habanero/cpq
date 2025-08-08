from pathlib import Path
from typing import Final, Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=False, extra="ignore"
    )

    BASE_DIR: Final[Path] = Path(__file__).parent.parent.parent
    CORS_ORIGINS: list[str] = Field(
        default=["http://localhost:5173"],
        description="Allowed CORS origins"
    )
    CORS_ALLOW_CREDENTIALS: bool = Field(
        default=True,
        description="Allow credentials in CORS requests"
    )
    ENVIRONMENT: Literal["development", "production"] = Field(
        default="development", description="Application environment"
    )

    LOG_LEVEL: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = Field(
        default="INFO", description="Logging level"
    )
    STRUCTURED_LOGGING_ENABLED: bool = Field(default=False, description="Use JSON logging format")

settings = Settings()
