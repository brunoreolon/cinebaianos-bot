from src.bot.domain.repositories.maintenance_repository import MaintenanceRepository

class MaintenanceRepositorySQLite(MaintenanceRepository):

    def __init__(self, conn_provider):
        self.conn_provider = conn_provider

    def limpar_banco_filmes(self):
        with self.conn_provider.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM votos")
            cursor.execute("DELETE FROM filmes")
            cursor.execute("DELETE FROM sqlite_sequence WHERE name = 'filmes'")
            cursor.execute("DELETE FROM sqlite_sequence WHERE name = 'votos'")
            conn.commit()