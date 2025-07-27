import discord

from discord.ext import commands

from src.bot.di.repository_factory import criar_usuarios_repository

class Usuarios(commands.Cog):

    def __init__(self, bot, conn_provider):
        self.bot = bot
        self.usuario_repo = criar_usuarios_repository(conn_provider)

    @commands.command(name="registrar")
    async def registrar(self, ctx, *args):
        if len(args) < 2:
            await ctx.send("❌ Uso incorreto. Use: `!registrar <aba> <coluna>`")
            return

        aba = " ".join(args[:-1])  # Tudo menos o último é a aba
        coluna = args[-1]

        discord_id = str(ctx.author.id)
        nome = ctx.author.display_name

        # if buscar_usuario(discord_id):
        #     await ctx.send(f"{ctx.author.mention} você já está registrado.")
        # else:
        self.usuario_repo.registrar_usuario(discord_id, nome, aba, coluna)
        await ctx.send(f"✅ {ctx.author.mention} registrado com sucesso!\n🗂️ Aba: **{aba}** | 📊 Coluna: **{coluna}**")

    @commands.command(name="perfil")
    async def perfil(self, ctx, membro: discord.Member = None):
        membro = membro or ctx.author
        usuario = self.usuario_repo.buscar_usuario(str(membro.id))

        if usuario:
            _, nome, aba, coluna = usuario
            await ctx.send(f"\n**Perfil de {membro.display_name}**\n🌐 Nome: `{nome}`\n🗂️ Aba: `{aba}`\n📊 Coluna: `{coluna}`")
        else:
            await ctx.send(f"{membro.mention} ainda não está registrado. Use `!registrar <aba> <coluna>`.")

    @commands.command(name="usuarios")
    async def listar_usuarios(self, ctx, *args):
        if args:
            await ctx.send("❌ Uso incorreto. O comando `!usuarios` não aceita argumentos.")
            return

        usuarios = self.usuario_repo.buscar_todos_os_usuarios()

        if not usuarios:
            await ctx.send("Nenhum usuário registrado.")
            return

        msg = "**👥 Usuários Registrados:**\n"
        for discord_id, nome, aba, coluna in usuarios:
            mention = f"<@{discord_id}>"
            msg += f"• {mention} — `{nome}` | Aba: `{aba}`, Coluna: `{coluna}`\n"

        await ctx.send(msg)

    @perfil.error
    async def perfil_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send("❌ Usuário não encontrado. Use: `!perfil [@usuário]` ou apenas `!perfil` para ver o seu.")
        else:
            raise error

async def setup(bot):
    conn_provider = getattr(bot, "conn_provider", None)
    await bot.add_cog(Usuarios(bot, conn_provider))