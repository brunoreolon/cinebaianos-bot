import discord
from discord.ext import commands
from src.bot.db.db import buscar_usuario, contar_generos_por_usuario, contar_generos_mais_assistidos, contar_generos_da_hora, contar_generos_lixo

class Generos(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="generos")
    async def generos(self, ctx, membro: discord.Member = None):
        if membro:
            usuario = buscar_usuario(str(membro.id))
            if not usuario:
                await ctx.send(f"{membro.mention} ainda não está registrado.")
                return
            generos_ordenados = contar_generos_por_usuario(usuario[0])
            if not generos_ordenados:
                await ctx.send(f"{membro.display_name} ainda não adicionou filmes com gêneros.")
                return
            titulo = f"🎬 Gêneros trazidos por {membro.display_name}"
        else:
            generos_ordenados = contar_generos_mais_assistidos()
            if not generos_ordenados:
                await ctx.send("Nenhum filme registrado.")
                return
            titulo = "🎞️ Gêneros mais assistidos"

        mensagem = f"**{titulo}:**\n"
        for genero, contagem in generos_ordenados:
            mensagem += f"• {genero}: {contagem} filmes\n"

        await ctx.send(mensagem)

    @commands.command(name="meus-generos")
    async def meus_generos(self, ctx):
        usuario = buscar_usuario(str(ctx.author.id))
        if not usuario:
            await ctx.send("Você precisa se registrar primeiro com `!registrar <aba> <coluna>`.")
            return

        generos_ordenados = contar_generos_por_usuario(usuario[0])
        if not generos_ordenados:
            await ctx.send("Você ainda não adicionou filmes com gêneros.")
            return

        mensagem = "**🎬 Seus gêneros mais frequentes:**\n"
        for genero, contagem in generos_ordenados:
            mensagem += f"• {genero}: {contagem} filmes\n"

        await ctx.send(mensagem)

    @commands.command(name="generos-da-hora")
    async def generos_da_hora(self, ctx):
        generos_ordenados = contar_generos_da_hora()

        if not generos_ordenados:
            await ctx.send("Nenhum voto DA HORA registrado.")
            return

        mensagem = "**🔥 Gêneros com mais votos DA HORA:**\n"
        for genero, contagem in generos_ordenados:
            mensagem += f"• {genero}: {contagem} votos\n"

        await ctx.send(mensagem)

    @commands.command(name="generos-lixo")
    async def generos_lixo(self, ctx):
        generos_ordenados = contar_generos_lixo()

        if not generos_ordenados:
            await ctx.send("Nenhum voto LIXO registrado.")
            return

        mensagem = "**🗑️ Gêneros com mais votos LIXO:**\n"
        for genero, contagem in generos_ordenados:
            mensagem += f"• {genero}: {contagem} votos\n"

        await ctx.send(mensagem)

async def setup(bot):
    await bot.add_cog(Generos(bot))