from pydantic_settings import BaseSettings
from pydantic import Field
from typing import List


class Settings(BaseSettings):
    # Authentication
    auth_secret_key: str = Field("observability", alias="AUTH_SECRET_KEY")
    auth_algorithm: str = Field("HS256", alias="AUTH_ALGORITHM")
    auth_exp: int = Field(9999999, alias="AUTH_EXP")

    # Modules
    modules: List[str] = Field(["admin", "observability"], alias="MODULES")

    # CORS
    cors_origins: List[str] = Field(
        ["http://localhost:3000", "http://localhost:5000", "http://localhost:5173"],
        alias="CORS_ORIGINS",
    )
    cors_methods: str = Field("*", alias="CORS_METHODS")
    cors_headers: str = Field("*", alias="CORS_HEADERS")

    # Routes
    backend_route: str = Field("http://localhost:5000", alias="BACKEND_ROUTE")
    frontend_route: str = Field("http://localhost:3000", alias="FRONTEND_ROUTE")

    # Database
    database_sync: str = Field(
        "postgresql://root:teste123@db/observability", alias="DATABASE_SYNC"
    )
    database: str = Field(
        "postgresql+asyncpg://root:teste123@db/observability", alias="DATABASE"
    )

    # Migrations
    migrations_dir: str = Field("/var/www/observability/app/migrations/json", alias="MIGRATIONS_DIR")

    # Project
    project_path: str = Field("app/", alias="PROJECT_PATH")
    debug: bool = Field(False, alias="DEBUG")

    # Project Info
    project_title: str = Field("Observability", alias="PROJECT_TITLE")
    project_description: str = Field(
        "FastAPI Template project | Under development", alias="PROJECT_DESCRIPTION"
    )
    project_version: str = Field("0.0.0", alias="PROJECT_VERSION")
    logo_path: str = Field("http://localhost:5000/index/logo", alias="LOGO_PATH")

    # Server
    server_host: str = Field("0.0.0.0", alias="SERVER_HOST")
    server_port: int = Field(5000, alias="SERVER_PORT")

settings = Settings()
