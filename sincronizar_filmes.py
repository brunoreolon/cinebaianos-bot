# sincronizar_filmes.py
import logging
from db import limpar_banco_filmes, adicionar_filme, registrar_voto, buscar_filme_por_linha_e_usuario
from sheets import ler_todos_os_filmes, ler_votos_da_planilha
from tmdb import buscar_detalhes_filme

def sincronizar_filmes_com_planilha():
    logging.info("🔄 Sincronizando filmes com a planilha...\n")

    logging.info("Limpando o banco...")
    limpar_banco_filmes()

    logging.info("\nLendo filmes da planiha...")
    filmes_planilha = ler_todos_os_filmes()
    total_filmes = 0

    # 3. Adicionar no banco com dados enriquecidos
    for filme in filmes_planilha:
        titulo = filme['titulo']
        ano = filme['ano']
        id_responsavel = filme['id_responsavel']
        id_linha = filme['id_linha']

        logging.info(f"\n🔍 Buscando: {titulo}")
        detalhes = buscar_detalhes_filme(titulo, ano)
        logging.info(f"Detalhes encontrados:\n{detalhes}")

        if detalhes:
            adicionar_filme(
                tmdb_id=detalhes.id,
                titulo=detalhes.title,
                id_responsavel=id_responsavel,
                linha_planilha=id_linha,
                ano=detalhes.ano,
                genero=detalhes.genres[0]["name"] if detalhes.genres else "Indefinido"
            )

            logging.info(f"✅ {detalhes.title} ({detalhes.ano}) adicionado.")
            total_filmes += 1
        else:
            logging.info(f"⚠️ Detalhes não encontrados: {detalhes.title} ({detalhes.ano})")

    return total_filmes


def sincronizar_votos_com_planilha():
    logging.info("\n🔄 Sincronizando votos com a planilha...\n")

    # 2. Carregar os votos da planilha
    votos = ler_votos_da_planilha()  # Cada item deve conter: id_linha, id_votante, id_responsavel, voto
    logging.info(f"\n📌 Total de votos encontrados: {len(votos)}")
    total_votos = 0

    for voto in votos:
        id_responsavel = voto["id_responsavel"]
        nome_responsavel = voto["nome_responsavel"]
        id_votante = voto["id_votante"]
        nome_votante = voto["nome_votante"]
        id_linha = voto["id_linha"]
        aba = voto["aba"]
        valor_voto = voto["voto"]

        logging.info(f"\n🔍 Processando voto: Aba={aba}, linha={id_linha}, votante={nome_votante}, responsavel={nome_responsavel}, voto={valor_voto}")

        filme_info = buscar_filme_por_linha_e_usuario(id_responsavel, id_linha)
        if not filme_info:
            logging.info(f"❌ Filme não encontrado para responsavel={nome_responsavel}, linha={id_linha}")
            continue

        id_filme, titulo_filme = filme_info
        registrar_voto(id_filme, id_responsavel, id_votante, valor_voto)
        logging.info(f"🗳️ Voto registrado: {nome_votante} votou '{valor_voto}' no filme '{titulo_filme}' (Aba={aba}, Responsável={nome_responsavel}, linha {id_linha})")
        total_votos += 1

    logging.info("\n✅ Sincronização de votos concluída.")
    return total_votos

def sincronizar_planilha():
    total_filmes = sincronizar_filmes_com_planilha()
    total_votos = sincronizar_votos_com_planilha()

    return total_filmes, total_votos

if __name__ == "__main__":
    sincronizar_filmes_com_planilha()
    sincronizar_votos_com_planilha()

    logging.info("\n✅ Sincronização concluída.")
    
