from abc import ABC, abstractmethod
from typing import List, Tuple

class VotosRepository(ABC):

    @abstractmethod
    def registrar_voto(self, id_filme: int, id_responsavel: str, id_votante: str, voto: str) -> None:
        pass

    @abstractmethod
    def contar_votos_recebidos_todos_usuario(self, discord_id: str, voto_tipo: str) -> int:
        pass

    @abstractmethod
    def contar_todos_os_votos_por_usuario(self) -> List[Tuple[str, int, int]]:
        pass
