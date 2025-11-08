import discord

from discord.ext import commands

from src.bot.exception.api_error import ApiError
from src.bot.utils.error_utils import get_error_message


class Generos(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.api_client = bot.api_client

    @commands.command(name="generos")
    async def generos(self, ctx, membro: discord.Member = None):
        try:
            if membro:
                resposta = await self.api_client.get(f"/genres/users/{membro.id}")
                titulo = f"🎬 Gêneros trazidos por {membro.display_name}"
            else:
                resposta = await self.api_client.get(f"/genres/rankings", params={"type": 1})
                titulo = f"🎞️ Gêneros mais assistidos"

            generos = resposta  # agora já é lista
        except ApiError as e:
            await ctx.send(f"❌ {e.message}")
            return

        if not generos:
            await ctx.send("Nenhum gênero registrado.")
            return

        mensagem = f"**{titulo}:**\n"
        for genero in generos:
            mensagem += f"• {genero.get("name")}: {genero.get("total")} filmes\n"

        await ctx.send(mensagem)

    @commands.command(name="meus-generos")
    async def meus_generos(self, ctx):
        try:
            resposta = await self.api_client.get(f"/genres/users/{str(ctx.author.id)}")
        except ApiError as e:
            await ctx.send(get_error_message(e.code, e.detail))
            return

        generos = resposta

        if not generos:
            await ctx.send("Você ainda não adicionou filmes com gêneros.")
            return

        mensagem = "**🎬 Seus gêneros mais frequentes:**\n"
        for genero in generos:
            mensagem += f"• {genero.get("name")}: {genero.get("total")} filmes\n"

        await ctx.send(mensagem)

    @commands.command(name="generos-da-hora")
    async def generos_da_hora(self, ctx):
        await self._generos_por_tipo(ctx, tipo=1, titulo_emoji="🔥", titulo_texto="DA HORA")

    @commands.command(name="generos-lixo")
    async def generos_lixo(self, ctx):
        await self._generos_por_tipo(ctx, tipo=2, titulo_emoji="🗑️", titulo_texto="LIXO")

    async def _generos_por_tipo(self, ctx, tipo: int, titulo_emoji: str, titulo_texto: str):
        try:
            resposta = await self.api_client.get("/genres/vote-counts", params={"type": tipo})
            generos = resposta
        except ApiError as e:
            await ctx.send(f"❌ {e.message}")
            return

        if not generos:
            await ctx.send(f"Nenhum voto {titulo_texto.upper()} registrado.")
            return

        mensagem = f"**{titulo_emoji} Gêneros com mais votos {titulo_texto.upper()}:**\n"

        for genero in generos:
            nome = genero["genre"]
            votos = genero.get("votes", [])
            total_votos = 0
            for voto in votos:
                if voto["type"]["id"] == tipo:
                    total_votos = voto["totalVotes"]
                    break
            mensagem += f"• {nome}: {total_votos} votos\n"

        await ctx.send(mensagem)

async def setup(bot):
    await bot.add_cog(Generos(bot))