import os
from dotenv import load_dotenv

load_dotenv()

from src.bot.domain.providers.connection_provider import ConnectionProvider
from src.bot.infra.sqlite.sqlite_connection_provider import SQLiteConnectionProvider

CONNECTIONS = {
    "sqlite": SQLiteConnectionProvider,
}

def get_connection_provider() -> ConnectionProvider:
    backend = os.getenv("DB_BACKEND").lower()
    try:
        return CONNECTIONS[backend]()
    except KeyError:
        raise ValueError(f"ConnectionProvider não suportado: {backend}")
