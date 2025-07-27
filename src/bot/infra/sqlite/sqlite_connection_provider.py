import sqlite3
import os

from src.bot.domain.providers.connection_provider import ConnectionProvider

class SQLiteConnectionProvider(ConnectionProvider):
    def __init__(self, db_path=None):
        self.db_path = db_path or os.getenv("DATABASE_PATH")
        if not self.db_path:
            raise ValueError("Caminho do banco de dados não definido. Defina a variável de ambiente DATABASE_PATH ou passe o caminho no construtor.")

    def get_connection(self):
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        return sqlite3.connect(self.db_path, check_same_thread=False)
