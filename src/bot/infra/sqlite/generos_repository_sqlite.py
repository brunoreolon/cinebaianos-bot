from typing import List, Tuple

from src.bot.domain.providers.connection_provider import ConnectionProvider
from src.bot.domain.repositories.generos_repository import GenerosRepository

class GenerosRepositorySQLite(GenerosRepository):

    def __init__(self,  conn_provider: ConnectionProvider):
        self.conn_provider = conn_provider

    def contar_generos_mais_assistidos(self) -> List[Tuple[str, int]]:
        with self.conn_provider.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT genero FROM filmes")
            linhas = cursor.fetchall()

        return self._contar_generos_a_partir_de_linhas(linhas)

    def contar_generos_da_hora(self) -> List[Tuple[str, int]]:
        with self.conn_provider.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                           SELECT f.genero
                           FROM votos v
                                    JOIN filmes f ON v.id_filme = f.id
                           WHERE v.voto = 'DA HORA'
                           """)
            linhas = cursor.fetchall()

        return self._contar_generos_a_partir_de_linhas(linhas)

    def contar_generos_lixo(self) -> List[Tuple[str, int]]:
        with self.conn_provider.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                           SELECT f.genero
                           FROM votos v
                                    JOIN filmes f ON v.id_filme = f.id
                           WHERE v.voto = 'LIXO'
                           """)
            linhas = cursor.fetchall()

        return self._contar_generos_a_partir_de_linhas(linhas)

    def contar_generos_por_usuario(self, id_usuario: str) -> List[Tuple[str, int]]:
        with self.conn_provider.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                           SELECT genero
                           FROM filmes
                           WHERE id_responsavel = ?
                           """, (id_usuario,))
            linhas = cursor.fetchall()

        return self._contar_generos_a_partir_de_linhas(linhas)

    def _contar_generos_a_partir_de_linhas(self, linhas: List[Tuple[str]]) -> List[Tuple[str, int]]:
        contagem = {}
        for linha in linhas:
            if not linha[0]:
                continue
            generos = [g.strip() for g in linha[0].split(",")]
            for genero in generos:
                contagem[genero] = contagem.get(genero, 0) + 1

        return sorted(contagem.items(), key=lambda x: x[1], reverse=True)