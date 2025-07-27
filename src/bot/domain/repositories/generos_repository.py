from abc import ABC, abstractmethod
from typing import List, Tuple

class GenerosRepository(ABC):

    @abstractmethod
    def contar_generos_mais_assistidos(self) -> List[Tuple[str, int]]:
        pass

    @abstractmethod
    def contar_generos_da_hora(self) -> List[Tuple[str, int]]:
        pass

    @abstractmethod
    def contar_generos_lixo(self) -> List[Tuple[str, int]]:
        pass

    @abstractmethod
    def contar_generos_por_usuario(self, id_usuario: str) -> List[Tuple[str, int]]:
        pass