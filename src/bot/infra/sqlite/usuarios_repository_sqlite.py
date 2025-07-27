from src.bot.domain.providers.connection_provider import ConnectionProvider
from src.bot.domain.repositories.usuarios_repository import UsuariosRepository

class UsuarioRepositorySQLite(UsuariosRepository):

    def __init__(self, conn_provider: ConnectionProvider):
        self.conn_provider = conn_provider

    def registrar_usuario(self, discord_id: str, nome: str, aba: str, coluna: str):
        with self.conn_provider.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO usuarios (discord_id, nome, aba, coluna)
                VALUES (?, ?, ?, ?)
            """, (discord_id, nome, aba, coluna))
            conn.commit()

    def buscar_todos_os_usuarios(self):
        with self.conn_provider.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM usuarios")
            return cursor.fetchall()

    def buscar_usuario(self, discord_id: str):
        with self.conn_provider.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                           SELECT discord_id, nome, aba, coluna
                           FROM usuarios
                           WHERE discord_id = ?
                           """, (discord_id,))
            return cursor.fetchone()
