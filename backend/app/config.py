import os
from dataclasses import dataclass
from functools import lru_cache

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    # Primary source: environment variables (or a single DATABASE_URL).
    db_user: str = os.getenv("DB_USER", "ksi_opinion_base")
    db_password: str = os.getenv("DB_PASSWORD", "ksi_opinion_base")
    db_host: str = os.getenv("DB_HOST", "localhost")
    db_port: str = os.getenv("DB_PORT", "5434")
    db_name: str = os.getenv("DB_NAME", "ksi_opinion_base")
    database_url: str | None = os.getenv("DATABASE_URL")

    @property
    def psycopg_dsn(self) -> str:
        if self.database_url:
            return self.database_url
        return (
            f"postgresql://{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )

    @property
    def sqlalchemy_dsn(self) -> str:
        raw = self.psycopg_dsn
        if raw.startswith("postgresql+psycopg://"):
            return raw
        if raw.startswith("postgresql://"):
            return raw.replace("postgresql://", "postgresql+psycopg://", 1)
        if raw.startswith("postgres://"):
            return raw.replace("postgres://", "postgresql+psycopg://", 1)
        return raw


@lru_cache
def get_settings() -> Settings:
    return Settings()
