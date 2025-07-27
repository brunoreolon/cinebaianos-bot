import os
import requests

from dotenv import load_dotenv

load_dotenv()
TMDB_API_KEY = os.getenv("TMDB_API_KEY")
BASE_URL = "https://api.themoviedb.org/3"

class Filme:
    def __init__(self, id, title, genres, poster_path, ano):
        self.id = id
        self.title = title
        self.genres = genres
        self.poster_path = poster_path
        self.ano = ano

    def __str__(self):
        genero = self.genres[0]["name"] if self.genres else "Indefinido"
        return (
            f"  - Filme: {self.title}\n"
            f"  - Ano: {self.ano}\n"
            f"  - ID TMDb: {self.id}\n"
            f"  - Gênero: {genero}"
        )

def buscar_detalhes_filme(titulo, ano):
    url = f"{BASE_URL}/search/movie"
    params = {
        "api_key": TMDB_API_KEY,
        "query": titulo,
        "year": ano,
        "language": "pt-BR"
    }
    response = requests.get(url, params=params)

    if response.status_code != 200:
        return None

    dados = response.json()
    resultados = dados.get("results")
    if not resultados:
        return None

    filme_id = resultados[0]["id"]

    # Buscar detalhes
    detalhes_url = f"{BASE_URL}/movie/{filme_id}"
    detalhes_params = {
        "api_key": TMDB_API_KEY,
        "language": "pt-BR"
    }
    detalhes_resp = requests.get(detalhes_url, params=detalhes_params)
    if detalhes_resp.status_code != 200:
        return None

    data = detalhes_resp.json()
    return Filme(
        id=data.get("id"),
        title=data.get("title"),
        genres=data.get("genres"),
        poster_path=data.get("poster_path"),
        ano=data.get("release_date", "").split("-")[0]
    )
