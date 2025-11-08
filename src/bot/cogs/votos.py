import discord
from discord.ext import commands

from src.bot.utils.error_utils import get_error_message
from src.bot.exception.api_error import ApiError


class Votos(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.api_client = bot.api_client

    @commands.command(name="votar")
    async def votar(self, ctx, id_filme: int = None, voto: int = None):
        # Validação dos argumentos
        if id_filme is None or voto is None:
            await ctx.send(
                "❌ Uso incorreto do comando.\n"
                "Formato correto:\n`!votar [id_filme] [voto]`\n\n"
                "**Votos possíveis:**\n"
                "`1 - DA HORA`\n"
                "`2 - LIXO`\n"
                "`3 - NÃO ASSISTI`"
            )
            return

        VOTOS_MAPA = {
            1: "DA HORA",
            2: "LIXO",
            3: "NÃO ASSISTI"
        }

        if voto not in VOTOS_MAPA:
            await ctx.send("⚠️ Voto inválido. Use:\n`1 - DA HORA`\n`2 - LIXO`\n`3 - NÃO ASSISTI`")
            return

        payload = {
            "voter": {
                "discordId": str(ctx.author.id)
            },
            "movie": {
                "id": id_filme
            },
            "vote": voto
        }

        try:
            resposta = await self.api_client.post(f"/votes", json=payload)
        except ApiError as e:
            await ctx.send(get_error_message(e.code, e.detail))
            return

        filme = resposta["movie"]["title"]
        voto_texto = VOTOS_MAPA[voto]

        await ctx.send(f"✅ Voto registrado com sucesso!\n"
                       f"🎬 Filme: `{filme}`\n"
                       f"🗳️ Voto: **{voto_texto}**")

    @commands.command(name="votos", help="Mostra os votos de um filme pelo ID.")
    async def votos(self, ctx, movie_id: int):
        try:
            resposta = await self.api_client.get(f"/votes/{movie_id}/votes")
        except ApiError as e:
            await ctx.send(get_error_message(e.code, e.detail))
            return

        movie = resposta["movie"]
        votes = resposta.get("votes", [])

        # 🎬 Embed principal com informações do filme
        embed_filme = discord.Embed(
            title=f"{movie['title']} ({movie['year']})",
            description=(
                f"🎭 **{movie.get('genre', 'Gênero indefinido')}**\n"
                f"👤 Escolhido por **{movie['chooser']['name']}**"
            ),
            color=discord.Color.blurple()
        )

        if movie.get("posterPath"):
            embed_filme.set_image(url=movie["posterPath"])

        embed_filme.set_footer(text=f"TMDB ID: {movie['tmdbId']} • Adicionado em {movie['dateAdded'][:10]}")

        # Envia o embed principal do filme
        await ctx.send(embed=embed_filme)

        # 🗳️ Se não há votos, informa
        if not votes:
            await ctx.send("📭 Nenhum voto registrado para este filme ainda.")
            return

        # 🎨 Cores dinâmicas para cada tipo de voto
        colors = {
            "Da Hora": 0x00FF00,       # verde
            "Lixo": 0xFF0000,          # vermelho
            "Não Assisti": 0xFFFF66,   # cinza
        }

        emojis = {
            "Da Hora": "🔥",
            "Lixo": "💩",
            "Não Assisti": "💤"
        }

        # Cria um embed individual para cada voto
        for v in votes:
            voter = v["voter"]
            vote = v["vote"]
            desc = vote["description"]

            # Procura o membro no cache do servidor
            member = discord.utils.get(ctx.guild.members, id=int(voter["discordId"]))
            avatar_url = member.display_avatar.url if member else None

            voto_embed = discord.Embed(
                description=f"{emojis.get(desc, '❓')} votou **{desc.upper()}**",
                color=colors.get(desc, discord.Color.greyple())
            )

            # Coloca o avatar à esquerda do nome usando set_author
            if member:
                voto_embed.set_author(name=member.display_name, icon_url=avatar_url)
            else:
                voto_embed.set_author(name=voter["name"])  # fallback caso não encontrado

            await ctx.send(embed=voto_embed)


async def setup(bot):
    await bot.add_cog(Votos(bot))