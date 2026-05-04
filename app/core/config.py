from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Enterprise AI Operations Assistant"
    app_version: str = "0.1.0"

    postgres_db: str = "aiops"
    postgres_user: str = "aiops"
    postgres_password: str = "aiops"
    postgres_host: str = "postgres"
    postgres_port: int = 5432

    redis_host: str = "redis"
    redis_port: int = 6379

    qdrant_host: str = "qdrant"
    qdrant_port: int = 6333
    qdrant_collection_name: str = "document_chunks"

    openai_api_key: str = ""
    embedding_model: str = "text-embedding-3-small"

    chat_model: str = "gpt-4.1-mini"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    @staticmethod
    def _is_running_in_docker() -> bool:
        return Path("/.dockerenv").exists()

    def _resolve_host(self, host: str) -> str:
        if self._is_running_in_docker():
            return host

        docker_service_hosts = {
            "postgres",
            "redis",
            "qdrant",
        }

        if host in docker_service_hosts:
            return "localhost"

        return host

    @property
    def resolved_postgres_host(self) -> str:
        return self._resolve_host(self.postgres_host)

    @property
    def resolved_redis_host(self) -> str:
        return self._resolve_host(self.redis_host)

    @property
    def resolved_qdrant_host(self) -> str:
        return self._resolve_host(self.qdrant_host)

    @property
    def database_url(self) -> str:
        return (
            f"postgresql://{self.postgres_user}:"
            f"{self.postgres_password}@{self.resolved_postgres_host}:"
            f"{self.postgres_port}/{self.postgres_db}"
        )


settings = Settings()
