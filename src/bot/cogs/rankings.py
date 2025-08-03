from discord.ext import commands

class Rankings(commands.Cog):

    def __init__(self, bot, conn_provider):
        self.bot = bot

    @commands.command(name="ranking")
    async def ranking(self, ctx):
        ranking = self.voto_repo.contar_todos_os_votos_por_usuario()

        if not ranking:
            await ctx.send("Nenhum voto registrado ainda.")
            return

        msg = "**📊 Ranking Geral:**\n"
        for nome, da_hora, lixo in ranking:
            msg += f"• **{nome}** — 🏆 DA HORA: `{da_hora}` | 🗑️ LIXO: `{lixo}`\n"

        await ctx.send(msg)

    @commands.command(name="da-hora")
    async def da_hora(self, ctx, *, argumento: str = None):
        voto_tipo = "DA HORA"

        # Se passou argumento, tenta interpretar como menção
        if argumento:
            try:
                membro = await commands.MemberConverter().convert(ctx, argumento)
            except commands.BadArgument:
                await ctx.send("❌ Argumento inválido. Use uma menção ao usuário (`@usuário`) ou deixe vazio para ver o ranking.")
                return

            usuario = self.usuario_repo.buscar_usuario(str(membro.id))
            if not usuario:
                await ctx.send(f"{membro.mention} ainda não está registrado.")
                return

            total = self.voto_repo.contar_votos_recebidos_todos_usuario(str(membro.id), voto_tipo)
            await ctx.send(f"🏆 {membro.display_name} recebeu **{total}** votos *DA HORA*.")
            return

        # Sem argumento: ranking completo
        usuarios = self.usuario_repo.buscar_todos_os_usuarios()
        if not usuarios:
            await ctx.send("Nenhum usuário registrado ainda.")
            return

        ranking = []
        for discord_id, nome, _, _ in usuarios:
            total = self.voto_repo.contar_votos_recebidos_todos_usuario(discord_id, voto_tipo)
            ranking.append((nome, total))

        # Ordenar por quantidade de votos decrescente
        ranking.sort(key=lambda x: x[1], reverse=True)

        msg = "**🏆 Ranking — Top DA HORA:**\n"
        for i, (nome, total) in enumerate(ranking, 1):
            msg += f"{i}. **{nome}** — {total} votos\n"
        await ctx.send(msg)

    @commands.command(name="lixos")
    async def lixos(self, ctx, *, argumento: str = None):
        voto_tipo = "LIXO"

        if argumento:
            try:
                membro = await commands.MemberConverter().convert(ctx, argumento)
            except commands.BadArgument:
                await ctx.send("❌ Argumento inválido. Use uma menção ao usuário (`@usuário`) ou deixe vazio para ver o ranking.")
                return

            usuario = self.usuario_repo.buscar_usuario(str(membro.id))
            if not usuario:
                await ctx.send(f"{membro.mention} ainda não está registrado.")
                return

            total = self.voto_repo.contar_votos_recebidos_todos_usuario(str(membro.id), voto_tipo)
            await ctx.send(f"🗑️ {membro.display_name} recebeu **{total}** votos *LIXO*.")
            return

        usuarios = self.usuario_repo.buscar_todos_os_usuarios()
        if not usuarios:
            await ctx.send("Nenhum usuário registrado ainda.")
            return

        ranking = []
        for discord_id, nome, _, _ in usuarios:
            total = self.voto_repo.contar_votos_recebidos_todos_usuario(discord_id, voto_tipo)
            ranking.append((nome, total))

        ranking.sort(key=lambda x: x[1], reverse=True)

        msg = "**🗑️ Ranking — Top Lixos:**\n"
        for i, (nome, total) in enumerate(ranking, 1):
            msg += f"{i}. **{nome}** — {total} votos\n"
        await ctx.send(msg)

async def setup(bot):
    conn_provider = getattr(bot, "conn_provider", None)
    await bot.add_cog(Rankings(bot, conn_provider))