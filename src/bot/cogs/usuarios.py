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
        if len(args) < 1:
            await ctx.send("❌ Uso incorreto. Use: `!registrar [email]`")
            return

        discord_id = str(ctx.author.id)
        nome = ctx.author.display_name
        email = args[0]

        payload = {
            "discordId": discord_id,
            "name": nome,
            "email": email
        }

        try:
            resposta = await self.api_client.post("/users", json=payload)
        except ApiError as e:
            await ctx.send(f"{ctx.author.mention} " + get_error_message(e.code, e.detail))
            return

        await ctx.send(f"✅ {ctx.author.mention} registrado com sucesso!\n🌐 Nome: **{nome}**\n📧 Email: **{resposta['email']}**")


    @commands.command(name="perfil")
    async def perfil(self, ctx, membro: discord.Member = None):
        membro = membro or ctx.author

        try:
            usuario = await self.api_client.get(f"/users/{str(membro.id)}")
        except ApiError as e:
            await ctx.send(get_error_message(e.code, e.detail))
            return

        if usuario:
            discord_id = str(usuario["discordId"])
            nome = usuario["name"]
            email = usuario["email"]

            await ctx.send(
                f"\n**Perfil de {membro.display_name}**\n"
                f"🆔 Discord ID: `{discord_id}`\n"
                f"🌐 Nome: `{nome}`\n"
                f"📧 Email: `{email}`\n"
            )
        else:
            await ctx.send(f"{membro.mention} ainda não está registrado. Use `!registrar [aba] [coluna]`.")

    @commands.command(name="usuarios")
    async def listar_usuarios(self, ctx, *args):
        if args:
            await ctx.send("❌ Uso incorreto. O comando `!usuarios` não aceita argumentos.")
            return

        try:
            usuarios = await self.api_client.get(f"/users")
        except ApiError as e:
            await ctx.send(get_error_message(e.code, e.detail))
            return

        if not usuarios:
            await ctx.send("Nenhum usuário registrado.")
            return

        msg = "**👥 Usuários Registrados:**\n\n"
        for usuario in usuarios:

            nome = usuario["name"]
            email = usuario.get("email")
            discord_id = usuario["discordId"]

            mention = f"<@{discord_id}>"
            msg += f"• {mention} — 🆔 `{discord_id}` — 🌐 `{nome}` — 📧 `{email}`\n"

        await ctx.send(msg)

async def setup(bot):
    await bot.add_cog(Usuarios(bot))