import discord

class EmbedUtils:

    @staticmethod
    def filme_adicionado_embed(tmdb_id, responsavel, titulo, ano, genero, poster, color):
        """Gera um embed reutilizável para exibir informações de filme."""
        embed = discord.Embed(
            title=titulo,
            description=f"Ano: {ano}\nGênero: {genero}",
            color=color
        )

        if poster:
            embed.set_image(url=poster)

        embed.set_footer(
            text=f"Responsável: {responsavel}\n"
                 f"ID do Filme: {tmdb_id}"
        )

        return embed

    @staticmethod
    def lista_filmes_embed(responsavel, total_filmes, color, avatar, lista_formatada):
        """Gera uma lista de filmes."""
        embed = discord.Embed(
            title=f"🎬 Filmes adicionados por {responsavel} (Total: {total_filmes})",
            color=color
        )

        if avatar:
            embed.set_thumbnail(url=avatar)

        embed.description = lista_formatada

        return embed

    @staticmethod
    def criar_embed_filme_dropdown(filme):
        embed = discord.Embed(
            title=f"{filme['title']} ({filme['releaseDate'][:4]})",
            description=f"TMDb ID: `{filme['id']}`\nData de lançamento: {filme['releaseDate']}",
            color=discord.Color.blurple()
        )
        if filme.get("posterPath"):
            embed.set_thumbnail(url=filme["posterPath"])

        return embed