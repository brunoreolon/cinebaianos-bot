# db.py
import sqlite3
import os
from datetime import datetime
import logging

DB_PATH = os.getenv("DATABASE_PATH", "./data/filmes.db")

def conectar():
    caminho = os.path.abspath(DB_PATH)
    # logging.info(f"🔗 Conectando ao banco em: {caminho}")
    return sqlite3.connect(DB_PATH)

def criar_tabelas():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        discord_id TEXT PRIMARY KEY,
        nome TEXT,
        aba TEXT,
        coluna TEXT
    )""")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS filmes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT,
        id_responsavel TEXT,
        linha_planilha INTEGER,
        genero TEXT, 
        ano INTEGER,
        tmdb_id INTEGER,
        data_adicionado TEXT,
        FOREIGN KEY(id_responsavel) REFERENCES usuarios(discord_id)
    )""")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS votos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_filme INTEGER,
        id_responsavel TEXT,
        id_votante TEXT,
        voto TEXT,
        FOREIGN KEY(id_filme) REFERENCES filmes(id),
        FOREIGN KEY(id_responsavel) REFERENCES usuarios(discord_id),
        FOREIGN KEY(id_votante) REFERENCES usuarios(discord_id),
        UNIQUE(id_filme, id_votante)
    )""")

    conn.commit()
    conn.close()

def registrar_usuario(discord_id, nome, aba, coluna):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR REPLACE INTO usuarios (discord_id, nome, aba, coluna)
        VALUES (?, ?, ?, ?)
    """, (discord_id, nome, aba, coluna))
    conn.commit()
    conn.close()

def buscar_usuario(discord_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE discord_id = ?", (discord_id,))
    resultado = cursor.fetchone()
    conn.close()
    return resultado

def buscar_todos_os_usuarios():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT discord_id, nome, aba, coluna FROM usuarios")
    resultado = cursor.fetchall()
    conn.close()
    return resultado

def adicionar_filme(titulo, id_responsavel, linha_planilha, genero, ano, tmdb_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO filmes (titulo, id_responsavel, linha_planilha, genero, ano, tmdb_id, data_adicionado)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (titulo, id_responsavel, linha_planilha, genero, ano, tmdb_id, datetime.now().isoformat()))
    conn.commit()
    filme_id = cursor.lastrowid
    conn.close()
    return filme_id

def registrar_voto(id_filme, id_responsavel, id_votante, voto):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO votos (id_filme, id_responsavel, id_votante, voto)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(id_filme, id_votante) DO UPDATE SET voto=excluded.voto
    """, (id_filme, id_responsavel, id_votante, voto))
    conn.commit()
    conn.close()

def buscar_filmes_por_usuario(discord_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM filmes WHERE id_responsavel = ?", (discord_id,))
    filmes = cursor.fetchall()
    conn.close()
    return filmes

def buscar_filme_por_linha_e_usuario(id_responsavel, linha_planilha):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, titulo FROM filmes
        WHERE id_responsavel = ? AND linha_planilha = ?
    """, (id_responsavel, linha_planilha))
    resultado = cursor.fetchone()
    conn.close()
    return resultado

def buscar_filme_por_linha(linha_planilha):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM filmes WHERE linha_planilha = ?", (linha_planilha,))
    filme = cursor.fetchone()
    conn.close()
    return filme

import sqlite3

def buscar_todos_os_filmes():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM filmes ORDER BY id_responsavel, linha_planilha")
    filmes = cursor.fetchall()
    conn.close()
    return filmes

def contar_votos_por_tipo(voto_tipo: str):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT usuarios.nome, COUNT(*) as total
        FROM votos
        JOIN usuarios ON votos.id_votante = usuarios.discord_id
        WHERE votos.voto = ?
        GROUP BY votos.id_votante
        ORDER BY total DESC
    """, (voto_tipo,))
    resultados = cursor.fetchall()
    conn.close()
    return resultados

def contar_votos_recebidos_todos_usuario(discord_id: str, voto_tipo: str):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT COUNT(*)
        FROM filmes f
        JOIN votos v ON f.id = v.id_filme
        WHERE f.id_responsavel = ? AND v.voto = ?
    """, (discord_id, voto_tipo))
    resultado = cursor.fetchone()
    conn.close()
    return resultado[0] if resultado else 0


def contar_todos_os_votos_por_usuario():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT u.nome,
               SUM(CASE WHEN v.voto = 'DA HORA' THEN 1 ELSE 0 END) AS da_hora,
               SUM(CASE WHEN v.voto = 'LIXO' THEN 1 ELSE 0 END) AS lixo
        FROM usuarios u
        LEFT JOIN filmes f ON u.discord_id = f.id_responsavel
        LEFT JOIN votos v ON f.id = v.id_filme
        GROUP BY u.nome
        ORDER BY da_hora DESC
    """)
    resultado = cursor.fetchall()
    conn.close()
    return resultado

def contar_generos_mais_assistidos():
    conn = conectar()
    cursor = conn.cursor()
    
    cursor.execute("SELECT genero FROM filmes")
    linhas = cursor.fetchall()
    conn.close()

    contagem_generos = {}
    for linha in linhas:
        if not linha[0]:
            continue
        generos = [g.strip() for g in linha[0].split(",")]
        for genero in generos:
            contagem_generos[genero] = contagem_generos.get(genero, 0) + 1

    generos_ordenados = sorted(contagem_generos.items(), key=lambda x: x[1], reverse=True)
    return generos_ordenados

def contar_generos_da_hora():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT f.genero
        FROM votos v
        JOIN filmes f ON v.id_filme = f.id
        WHERE v.voto = 'DA HORA'
    """)
    linhas = cursor.fetchall()
    conn.close()

    contagem_generos = {}
    for linha in linhas:
        if not linha[0]:
            continue
        generos = [g.strip() for g in linha[0].split(",")]
        for genero in generos:
            contagem_generos[genero] = contagem_generos.get(genero, 0) + 1

    generos_ordenados = sorted(contagem_generos.items(), key=lambda x: x[1], reverse=True)
    return generos_ordenados

def contar_generos_lixo():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT f.genero
        FROM votos v
        JOIN filmes f ON v.id_filme = f.id
        WHERE v.voto = 'LIXO'
    """)
    linhas = cursor.fetchall()
    conn.close()

    contagem_generos = {}
    for linha in linhas:
        if not linha[0]:
            continue
        generos = [g.strip() for g in linha[0].split(",")]
        for genero in generos:
            contagem_generos[genero] = contagem_generos.get(genero, 0) + 1

    generos_ordenados = sorted(contagem_generos.items(), key=lambda x: x[1], reverse=True)
    return generos_ordenados

def contar_generos_por_usuario(id_usuario):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT genero
        FROM filmes
        WHERE id_responsavel = ?
    """, (id_usuario,))
    linhas = cursor.fetchall()
    conn.close()

    contagem = {}
    for linha in linhas:
        if not linha[0]:
            continue
        generos = [g.strip() for g in linha[0].split(",")]
        for genero in generos:
            contagem[genero] = contagem.get(genero, 0) + 1

    return sorted(contagem.items(), key=lambda x: x[1], reverse=True)

def limpar_banco_filmes():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM votos")
    cursor.execute("DELETE FROM filmes")
    conn.commit()
    conn.close()

def buscar_id_filme_por_linha(id_linha):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id, titulo FROM filmes WHERE linha_planilha = ?", (id_linha,))
    resultado = cursor.fetchone()
    conn.close()
    return resultado if resultado else None