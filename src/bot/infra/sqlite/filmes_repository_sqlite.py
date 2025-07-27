from typing import List, Optional, Tuple

from src.bot.domain.providers.connection_provider import ConnectionProvider
from src.bot.domain.repositories.filmes_repository import FilmesRepository

class FilmesRepositorySQLite(FilmesRepository):

    def __init__(self, conn_provider: ConnectionProvider):
        self.conn_provider = conn_provider

    def adicionar_filme(self, titulo: str, id_responsavel: str, linha_planilha: int,
                        genero: str, ano: int, tmdb_id: int) -> int:
        with self.conn_provider.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                           INSERT INTO filmes (titulo, id_responsavel, linha_planilha, genero, ano, tmdb_id, data_adicionado)
                           VALUES (?, ?, ?, ?, ?, ?, datetime('now'))
                           """, (titulo, id_responsavel, linha_planilha, genero, ano, tmdb_id))
            conn.commit()
            return cursor.lastrowid

    def buscar_filmes_por_usuario(self, discord_id: str) -> List[Tuple]:
        with self.conn_provider.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM filmes WHERE id_responsavel = ?", (discord_id,))
            return cursor.fetchall()

    def buscar_filme_por_linha_e_usuario(self, id_responsavel: str, linha_planilha: int) -> Optional[Tuple]:
        with self.conn_provider.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                           SELECT id, titulo FROM filmes
                           WHERE id_responsavel = ? AND linha_planilha = ?
                           """, (id_responsavel, linha_planilha))
            return cursor.fetchone()

    def buscar_filme_por_id(self, id_filme: int) -> Optional[Tuple]:
        with self.conn_provider.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM filmes WHERE id = ?", (id_filme,))
            return cursor.fetchone()

    def buscar_todos_os_filmes(self) -> List[Tuple]:
        with self.conn_provider.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM filmes ORDER BY id_responsavel, linha_planilha")
            return cursor.fetchall()