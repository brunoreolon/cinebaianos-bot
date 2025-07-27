import asyncio

from discord.ext import commands

from src.bot.sincronizar_filmes import sincronizar_planilha

class Sincronizacao(commands.Cog):

    def __init__(self, bot, conn_provider):
        self.bot = bot
        self.conn_provider = conn_provider

    @commands.command(name='sincronizar')
    @commands.has_permissions(administrator=True)
    async def sincronizar(self, ctx):
        await ctx.send("🔄 Iniciando **sincronização** com a planilha... Isso pode levar alguns segundos.")

        try:
            await ctx.send("📥 Lendo filmes e atualizando banco de dados...")
            total_filmes, total_votos, elapsed = await asyncio.to_thread(
                sincronizar_planilha, self.conn_provider
            )

            minutos = int(elapsed // 60)
            segundos = int(elapsed % 60)

            await ctx.send(
                f"✅ **Sincronização concluída com sucesso em {minutos} minutos e {segundos} segundos!**\n\n"
                f"🎬 Filmes Sincronizados: **{total_filmes}**\n"
                f"🗳️ Votos Registrados: **{total_votos}**"
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
    conn_provider = getattr(bot, "conn_provider", None)
    await bot.add_cog(Sincronizacao(bot, conn_provider))