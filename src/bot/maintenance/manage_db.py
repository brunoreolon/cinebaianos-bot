import logging
from src.bot.di.schemas_factory import get_schemas_repository

logging.basicConfig(level=logging.INFO)

def main():
    criar_tabelas = get_schemas_repository()
    criar_tabelas()
    logging.info("Tabelas criadas com sucesso!")

if __name__ == "__main__":
    main()