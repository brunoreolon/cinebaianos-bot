from abc import ABC, abstractmethod

class MaintenanceRepository(ABC):

    @abstractmethod
    def limpar_banco_filmes(self):
        pass