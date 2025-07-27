from abc import ABC, abstractmethod

class ConnectionProvider(ABC):

    @abstractmethod
    def get_connection(self):
        pass