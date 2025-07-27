from abc import ABC, abstractmethod

class SchemasRepository(ABC):

    @abstractmethod
    def criar_tabelas(self):
        pass