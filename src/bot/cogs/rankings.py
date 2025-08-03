from discord.ext import commands

from src.bot.exception.api_error import ApiError
from src.bot.utils.error_utils import get_error_message


class Rankings(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.api_client = bot.api_client

    @commands.command(name="ranking")
    async def ranking(self, ctx):
        try:
            resposta = await self.api_client.get(f"/ranking")
        except ApiError as e:
            await ctx.send(get_error_message(e.code, e.message))
            return

        if not resposta:
            await ctx.send("Nenhum voto registrado ainda.")
            return

        msg = "**📊 Ranking Geral:**\n"
        for usuario_votos in resposta:
            usuario = usuario_votos["user"]
            msg += f"• **{usuario['name']}** — 🏆 DA HORA: `{usuario_votos['total_da_hora']}` | 🗑️ LIXO: `{usuario_votos['total_lixo']}`\n"

        await ctx.send(msg)

    @commands.command(name="da-hora")
    async def da_hora(self, ctx, *, argumento: str = None):
        # Se passou argumento, tenta interpretar como menção
        if argumento:
            try:
                membro = await commands.MemberConverter().convert(ctx, argumento)
            except commands.BadArgument:
                await ctx.send("❌ Argumento inválido. Use uma menção ao usuário (`@usuário`) ou deixe vazio para ver o ranking.")
                return

            try:
                resposta = await self.api_client.get(f"/ranking/da-hora/{str(membro.id)}")
            except ApiError as e:
                await ctx.send(get_error_message(e.code, e.message))
                return

            await ctx.send(f"🏆 {membro.display_name} recebeu **{resposta['total_da_hora']}** votos *DA HORA*.")
            return

        # Sem argumento: ranking completo
        try:
            resposta = await self.api_client.get(f"/ranking/da-hora")
        except ApiError as e:
            await ctx.send(get_error_message(e.code, e.message))
            return

        msg = "**🏆 Ranking — Top DA HORA:**\n"
        for i, usuario_ranking in enumerate(resposta, start=1):
            usuario = usuario_ranking["user"]
            msg += f"{i}. **{usuario['name']}** — {usuario_ranking['total_da_hora']} votos\n"

        await ctx.send(msg)

    @commands.command(name="lixos")
    async def lixos(self, ctx, *, argumento: str = None):
        if argumento:
            try:
                membro = await commands.MemberConverter().convert(ctx, argumento)
            except commands.BadArgument:
                await ctx.send("❌ Argumento inválido. Use uma menção ao usuário (`@usuário`) ou deixe vazio para ver o ranking.")
                return

            try:
                resposta = await self.api_client.get(f"/ranking/lixos/{str(membro.id)}")
            except ApiError as e:
                await ctx.send(get_error_message(e.code, e.message))
                return

            await ctx.send(f"🗑️ {membro.display_name} recebeu **{resposta['total_lixo']}** votos *LIXO*.")
            return

        try:
            resposta = await self.api_client.get(f"/ranking/lixo")
        except ApiError as e:
            await ctx.send(get_error_message(e.code, e.message))
            return

        msg = "**🗑️ Ranking — Top Lixos:**\n"
        for i, usuario_ranking in enumerate(resposta, 1):
            usuario = usuario_ranking["user"]
            msg += f"{i}. **{usuario['name']}** — {usuario_ranking['total_lixo']} votos\n"

        await ctx.send(msg)

async def setup(bot):
    await bot.add_cog(Rankings(bot))