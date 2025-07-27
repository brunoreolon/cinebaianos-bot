from abc import ABC, abstractmethod
from typing import List, Optional, Tuple, Dict

class FilmesRepository(ABC):

    @abstractmethod
    def adicionar_filme(self, titulo: str, id_responsavel: str, linha_planilha: int,
                        genero: str, ano: int, tmdb_id: int) -> int:
        pass

    @abstractmethod
    def buscar_filmes_por_usuario(self, discord_id: str) -> List[Tuple]:
        pass

    @abstractmethod
    def buscar_filme_por_linha_e_usuario(self, id_responsavel: str, linha_planilha: int) -> Optional[Tuple]:
        pass

    @abstractmethod
    def buscar_filme_por_id(self, id_filme: int) -> Optional[Tuple]:
        pass

    @abstractmethod
    def buscar_todos_os_filmes(self) -> List[Tuple]:
        pass
