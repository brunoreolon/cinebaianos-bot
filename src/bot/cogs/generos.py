import discord

from discord.ext import commands
from discord import Embed

from src.bot.utils.date_utils import DateUtils
from src.bot.exception.api_error import ApiError
from src.bot.utils.error_utils import get_error_message


class Generos(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.api_client = bot.api_client

    def build_embed(self, title: str, description: str, fields: list[tuple], color: int = 0x3498db, ctx=None):
        """Cria embed com campos dinâmicos"""
        embed = Embed(title=title, description=description, color=color)
        for name, value in fields:
            embed.add_field(name=name, value=value, inline=True)
        if ctx:
            embed.set_footer(text=f"Consultado por {ctx.author.display_name} • {DateUtils.now_br_format()}")
        return embed

    @commands.command(name="generos")
    async def generos(self, ctx, membro: discord.Member = None):
        try:
            if membro:
                resposta = await self.api_client.get(f"/genres/users/{membro.id}")
                titulo = f"🎬 Gêneros trazidos por {membro.display_name}"
            else:
                resposta = await self.api_client.get(f"/genres/rankings", params={"type": 1})
                titulo = f"🎞️ Gêneros mais assistidos"

            generos = resposta
        except ApiError as e:
            await ctx.send(get_error_message(e.code, e.detail))
            return

        if not generos:
            await ctx.send("Nenhum gênero registrado.")
            return

        fields = [(g["name"], f"{g.get('total', 0)} filmes") for g in generos]
        embed = self.build_embed(title=titulo, description="", fields=fields, ctx=ctx)
        await ctx.send(embed=embed)

    @commands.command(name="meus-generos")
    async def meus_generos(self, ctx):
        try:
            resposta = await self.api_client.get(f"/genres/users/{str(ctx.author.id)}")
            generos = resposta
        except ApiError as e:
            await ctx.send(get_error_message(e.code, e.detail))
            return

        if not generos:
            await ctx.send("Você ainda não adicionou filmes com gêneros.")
            return

        fields = [(g["name"], f"{g.get('total', 0)} filmes") for g in generos]
        embed = self.build_embed(title="🎬 Seus gêneros mais frequentes", description="", fields=fields, ctx=ctx)
        await ctx.send(embed=embed)

    @commands.command(name="generos-da-hora")
    async def generos_da_hora(self, ctx):
        await self._generos_por_tipo(ctx, tipo=1, titulo_emoji="🔥", titulo_texto="DA HORA", color=0xf1c40f)

    @commands.command(name="generos-lixo")
    async def generos_lixo(self, ctx):
        await self._generos_por_tipo(ctx, tipo=2, titulo_emoji="🗑️", titulo_texto="LIXO", color=0xe74c3c)

    async def _generos_por_tipo(self, ctx, tipo: int, titulo_emoji: str, titulo_texto: str, color: int):
        try:
            resposta = await self.api_client.get("/genres/vote-counts", params={"type": tipo})
            generos = resposta
        except ApiError as e:
            await ctx.send(get_error_message(e.code, e.detail))
            return

        if not generos:
            await ctx.send(f"Nenhum voto {titulo_texto.upper()} registrado.")
            return

        fields = []
        for genero in generos:
            nome = genero["genre"]
            votos = genero.get("votes", [])
            total_votos = sum(v["totalVotes"] for v in votos if v["type"]["id"] == tipo)
            fields.append((nome, f"{total_votos} votos"))

        embed = self.build_embed(
            title=f"{titulo_emoji} Gêneros com mais votos {titulo_texto.upper()}",
            description="",
            fields=fields,
            color=color,
            ctx=ctx
        )
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Generos(bot))