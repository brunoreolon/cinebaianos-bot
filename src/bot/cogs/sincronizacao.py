from discord.ext import commands
from src.bot.sincronizar_filmes import sincronizar_planilha

class Sincronizacao(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='sincronizar')
    @commands.has_permissions(administrator=True)
    async def sincronizar(self, ctx):
        await ctx.send("🔄 Iniciando **sincronização** com a planilha... Isso pode levar alguns segundos.")

        try:
            await ctx.send("📥 Lendo filmes e atualizando banco de dados...")
            total_filmes, total_votos = sincronizar_planilha()

            await ctx.send(
                f"✅ **Sincronização concluída com sucesso!**\n\n"
                f"🎬 Filmes sincronizados: **{total_filmes}**\n"
                f"🗳️ Votos registrados: **{total_votos}**"
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