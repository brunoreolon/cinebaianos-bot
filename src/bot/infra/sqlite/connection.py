import sqlite3
import os

DB_PATH = os.getenv("DATABASE_PATH")

def criar_conexao():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    return sqlite3.connect(DB_PATH)