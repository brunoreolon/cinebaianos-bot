from discord.ext import commands

from src.bot.utils.error_utils import get_error_message
from src.bot.exception.api_error import ApiError

class Sincronizacao(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.api_client = bot.api_client

    @commands.command(name='sincronizar')
    @commands.has_permissions(administrator=True)
    async def sincronizar(self, ctx):
        await ctx.send("⚠️ O comando **sincronizar** foi desativado e não está mais disponível.")
        return

        await ctx.send("🔄 Iniciando **sincronização** com a planilha... Isso pode levar alguns segundos.")

        try:
            await ctx.send("📥 Lendo filmes e atualizando banco de dados...")

            try:
                resposta = await self.api_client.post("/sync")
            except ApiError as e:
                await ctx.send(get_error_message(e.code, e.detail))
                return

            elapsed = int(resposta["execution_time_seconds"])
            minutos = int(elapsed // 60)
            segundos = int(elapsed % 60)

            await ctx.send(
                f"✅ **Sincronização concluída com sucesso em {minutos} minutos e {segundos} segundos!**\n\n"
                f"🎬 Filmes Sincronizados: **{resposta['total_movie']}**\n"
                f"🗳️ Votos Registrados: **{resposta['total_votes']}**"
            )
        except Exception as e:
            await ctx.send(f"❌ Ocorreu um erro durante a sincronização:\n```{str(e)}```")

    @sincronizar.error
    async def sincronizar_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("❌ Você não tem permissão para usar este comando. Apenas administradores podem sincronizar a planilha.")
        else:
            raise error

async def setup(bot):
    await bot.add_cog(Sincronizacao(bot))