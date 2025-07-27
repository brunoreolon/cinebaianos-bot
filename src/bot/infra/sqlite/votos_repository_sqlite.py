from typing import List, Tuple

from src.bot.domain.providers.connection_provider import ConnectionProvider
from src.bot.domain.repositories.votos_repository import VotosRepository

class VotosRepositorySQLite(VotosRepository):

    def __init__(self,  conn_provider: ConnectionProvider):
        self.conn_provider = conn_provider

    def registrar_voto(self, id_filme: int, id_responsavel: str, id_votante: str, voto: str) -> None:
        with self.conn_provider.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                           INSERT INTO votos (id_filme, id_responsavel, id_votante, voto)
                           VALUES (?, ?, ?, ?)
                               ON CONFLICT(id_filme, id_votante) DO UPDATE SET voto=excluded.voto
                           """, (id_filme, id_responsavel, id_votante, voto))
            conn.commit()

    def contar_votos_recebidos_todos_usuario(self, discord_id: str, voto_tipo: str) -> int:
        with self.conn_provider.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                           SELECT COUNT(*)
                           FROM filmes f
                                    JOIN votos v ON f.id = v.id_filme
                           WHERE f.id_responsavel = ? AND v.voto = ?
                           """, (discord_id, voto_tipo))
            resultado = cursor.fetchone()
            return resultado[0] if resultado else 0

    def contar_todos_os_votos_por_usuario(self) -> List[Tuple[str, int, int]]:
        with self.conn_provider.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                           SELECT u.nome,
                                  SUM(CASE WHEN v.voto = 'DA HORA' THEN 1 ELSE 0 END) AS da_hora,
                                  SUM(CASE WHEN v.voto = 'LIXO' THEN 1 ELSE 0 END) AS lixo
                           FROM usuarios u
                                    LEFT JOIN filmes f ON u.discord_id = f.id_responsavel
                                    LEFT JOIN votos v ON f.id = v.id_filme
                           GROUP BY u.nome
                           ORDER BY da_hora DESC
                           """)
            return cursor.fetchall()
