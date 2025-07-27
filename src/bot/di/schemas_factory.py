import os
from dotenv import load_dotenv

load_dotenv()

from src.bot.domain.repositories.schemas_repository import SchemasRepository
from src.bot.infra.sqlite.schema_repository_sqlite import SchemasRepositorySQLite

SCHEMAS = {
    "sqlite": SchemasRepositorySQLite,
}

def get_schemas_repository(conn_provider) -> SchemasRepository:
    backend = os.getenv("DB_BACKEND").lower()

    try:
        return SCHEMAS[backend](conn_provider)
    except KeyError:
        raise ValueError(f"Schema para backend '{backend}' não suportado.")
