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
        if membro:
            try:
                resposta = await self.api_client.get(f"/genres/user/{str(membro.id)}")
            except ApiError as e:
                await ctx.send(get_error_message(e.code, e.message))
                return

            generos = resposta["genres"]

            if not resposta["genres"]:
                await ctx.send("Nenhum filme registrado.")
                return

            titulo = f"🎬 Gêneros trazidos por {membro.display_name}"
        else:
            try:
                resposta = await self.api_client.get(f"/genres/most-watched")
            except ApiError as e:
                await ctx.send(get_error_message(e.code, e.message))
                return

            generos = resposta["genres"]

            if not generos:
                await ctx.send("Nenhum filme registrado.")
                return

            titulo = "🎞️ Gêneros mais assistidos"

        mensagem = f"**{titulo}:**\n"
        for genero in generos:
            mensagem += f"• {genero['genre']}: {genero['count']} filmes\n"

        await ctx.send(mensagem)

    @commands.command(name="meus-generos")
    async def meus_generos(self, ctx):
        try:
            resposta = await self.api_client.get(f"/genres/mine", params={"discord_id": str(ctx.author.id)})
        except ApiError as e:
            await ctx.send(get_error_message(e.code, e.message))
            return

        generos = resposta["genres"]

        if not generos:
            await ctx.send("Você ainda não adicionou filmes com gêneros.")
            return

        mensagem = "**🎬 Seus gêneros mais frequentes:**\n"
        for genero in generos:
            mensagem += f"• {genero['genre']}: {genero['count']} filmes\n"

        await ctx.send(mensagem)

    @commands.command(name="generos-da-hora")
    async def generos_da_hora(self, ctx):
        try:
            resposta = await self.api_client.get(f"/genres/most-voted-good")
        except ApiError as e:
            await ctx.send(get_error_message(e.code, e.message))
            return

        generos = resposta["genres"]

        if not generos:
            await ctx.send("Nenhum voto DA HORA registrado.")
            return

        mensagem = "**🔥 Gêneros com mais votos DA HORA:**\n"
        for genero in generos:
            mensagem += f"• {genero['genre']}: {genero['count']} votos\n"

        await ctx.send(mensagem)

    @commands.command(name="generos-lixo")
    async def generos_lixo(self, ctx):
        try:
            resposta = await self.api_client.get(f"/genres/most-voted-bad")
        except ApiError as e:
            await ctx.send(get_error_message(e.code, e.message))
            return

        generos = resposta["genres"]

        if not generos:
            await ctx.send("Nenhum voto LIXO registrado.")
            return

        mensagem = "**🗑️ Gêneros com mais votos LIXO:**\n"
        for genero in generos:
            mensagem += f"• {genero['genre']}: {genero['count']} votos\n"

        await ctx.send(mensagem)

async def setup(bot):
    await bot.add_cog(Generos(bot))