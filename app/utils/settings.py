from enum import Enum
from typing import Set

from pydantic import BaseSettings, Field

from .constants import APP_VERSION


class LogLevel(str, Enum):
    CRITICAL = "CRITICAL"
    ERROR = "ERROR"
    WARNING = "WARNING"
    INFO = "INFO"
    DEBUG = "DEBUG"
    NOTSET = "NOTSET"


class EnvironmentEnum(str, Enum):
    PRODUCTION = "PRODUCTION"
    TEST = "TEST"
    DEVELOPMENT = "DEVELOPMENT"

    def is_test(self):
        return self == EnvironmentEnum.TEST


class Settings(BaseSettings):

    db_dsn: str = Field(
        ...,
        title="URI de conexão com o banco de dados",
    )

    openapi_path: str = Field(
        "/openapi.json",
        title=(
            "Caminho para exportar o OpenAPI, deixar vazio para não exportar."
        ),
    )

    title: str = Field("Onboarding API", title="Nome da aplicação")

    env: EnvironmentEnum = Field(
        EnvironmentEnum.PRODUCTION, title="Ambiente da aplicação"
    )

    cors_allow_origins: Set[str] = Field(
        default_factory=lambda: {"*"}, title="Origens liberadas para CORS"
    )

    logging_ignored_urls: Set[str] = Field(
        {"/api/v1/health"}, title="URLs para ignorar no log"
    )

    @property
    def version(self) -> str:
        """Versão da aplicação"""
        return APP_VERSION

    class Config:
        env_prefix = "APP_"
        env_file = ".env"
        env_file_encoding = "utf-8"
