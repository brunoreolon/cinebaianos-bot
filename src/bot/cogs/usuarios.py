import discord

from discord.ext import commands
from src.bot.exception.api_error import ApiError
from src.bot.utils.error_utils import get_error_message

class Usuarios(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.api_client = bot.api_client

    @commands.command(name="registrar")
    async def registrar(self, ctx, *args):
        if len(args) < 2:
            await ctx.send("❌ Uso incorreto. Use: `!registrar <aba> <coluna>`")
            return

        aba = " ".join(args[:-1])  # Tudo menos o último é a aba
        coluna = args[-1]

        discord_id = str(ctx.author.id)
        nome = ctx.author.display_name

        payload = {
            "discord_id": discord_id,
            "name": nome,
            "tab": aba,
            "column": coluna,
            "email": "bruno.reolonn@gmail.com",
            "password": "bruno1342"
        }

        try:
            resposta = await self.api_client.post("/users", json=payload)
        except ApiError as e:
            await ctx.send(f"{ctx.author.mention} " + get_error_message(e.code, e.message))
            return

        await ctx.send(f"✅ {ctx.author.mention} registrado com sucesso!\n🌐 Nome: **{nome}**\n📧 Email: **{resposta['email']}**\n🗂️ Aba: **{aba}**\n📊 Coluna: **{coluna}**")


    @commands.command(name="perfil")
    async def perfil(self, ctx, membro: discord.Member = None):
        membro = membro or ctx.author

        try:
            usuario = await self.api_client.get(f"/users/{str(membro.id)}")
        except ApiError as e:
            await ctx.send(e)
            return

        if usuario:
            nome = usuario["name"]
            aba = usuario["tab"]
            coluna = usuario["column"]
            email = usuario["email"]

            await ctx.send(f"\n**Perfil de {membro.display_name}**\n🌐 Nome: `{nome}`\n📧 Email: `{email}`\n🗂️ Aba: `{aba}`\n📊 Coluna: `{coluna}`")
        else:
            await ctx.send(f"{membro.mention} ainda não está registrado. Use `!registrar <aba> <coluna>`.")

    @commands.command(name="usuarios")
    async def listar_usuarios(self, ctx, *args):
        if args:
            await ctx.send("❌ Uso incorreto. O comando `!usuarios` não aceita argumentos.")
            return

        try:
            usuarios = await self.api_client.get(f"/users")
        except ApiError as e:
            await ctx.send(get_error_message(e.code, e.message))
            return

        if not usuarios:
            await ctx.send("Nenhum usuário registrado.")
            return

        msg = "**👥 Usuários Registrados:**\n\n"
        for usuario in usuarios:
            mention = f"<@{usuario['discord_id']}>"
            msg += f"• {mention} — `{usuario['name']}` | Aba: `{usuario['tab']}`, Coluna: `{usuario['column']}`\n"

        await ctx.send(msg)

    @perfil.error
    async def perfil_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send("❌ Usuário não encontrado. Use: `!perfil [@usuário]` ou apenas `!perfil` para ver o seu.")
        else:
            raise error

async def setup(bot):
    await bot.add_cog(Usuarios(bot))