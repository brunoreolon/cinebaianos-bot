import discord

from discord.ext import commands
from src.bot.config import Config
from src.bot.exception.api_error import ApiError
from discord.ext import commands
from src.bot.utils.permissions import is_admin_or_authorized


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.api_client = bot.api_client

    @commands.command(name="login")
    @commands.check(is_admin_or_authorized)
    async def registrar(self, ctx, *args):
        """Comando para forçar login manual na API."""
        try:
            message = await self.api_client.login()
            await ctx.send(f"🔑 {message}")
        except ApiError as e:
            await ctx.send(f"❌ Erro ao fazer login: {e.detail}")
        except Exception as e:
            await ctx.send(f"❌ Erro inesperado ao fazer login: {e}")

    @commands.command(name="refresh-token")
    @commands.check(is_admin_or_authorized)
    async def refresh_token(self, ctx):
        """Comando para o refresh manual."""
        try:
            message = await self.api_client.refresh_token_manual()
            await ctx.send(f"🔄 {message}")
        except ApiError as e:
            await ctx.send(f"❌ Erro ao fazer refresh: {e.detail}")
        except Exception as e:
            await ctx.send(f"❌ Erro inesperado ao fazer refresh: {e}")

    @commands.command(name="logout")
    @commands.check(is_admin_or_authorized)
    async def logout(self, ctx):
        """Comando para fazer logout."""
        try:
            message = await self.api_client.logout()
            await ctx.send(f"🚪 {message}")
        except ApiError as e:
            await ctx.send(f"❌ Erro ao fazer logout: {e.detail}")
        except Exception as e:
            await ctx.send(f"❌ Erro inesperado ao fazer logout: {e}")

async def setup(bot):
    await bot.add_cog(Admin(bot))