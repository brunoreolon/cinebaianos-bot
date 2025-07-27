from abc import ABC, abstractmethod
from typing import List, Tuple, Optional

class UsuariosRepository(ABC):

    @abstractmethod
    def registrar_usuario(self, discord_id: str, nome: str, aba: str, coluna: str) -> None:
        pass

    @abstractmethod
    def buscar_todos_os_usuarios(self) -> List[Tuple[str, str, str, str]]:
        pass

    @abstractmethod
    def buscar_usuario(self, discord_id: str) -> Optional[Tuple[str, str, str, str]]:
        pass