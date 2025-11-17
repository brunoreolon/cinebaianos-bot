import discord

from discord.ext import commands
from discord import Embed

from src.bot.config import Config
from src.bot.exception.api_error import ApiError
from discord.ext import commands
from src.bot.utils.permissions import is_admin_or_authorized
from src.bot.utils.date_utils import DateUtils


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.api_client = bot.api_client

    @staticmethod
    def build_status_embed(title: str, message: str, color: int, ctx):
        """Função auxiliar para criar embeds de status"""
        embed = Embed(
            title=title,
            description=message,
            color=color
        )
        embed.set_footer(text=f"Executado por {ctx.author.display_name} • {DateUtils.now_br_format()}")
        return embed

    @commands.command(name="login")
    @commands.check(is_admin_or_authorized)
    async def login(self, ctx, *args):
        """Comando para forçar login manual na API."""
        try:
            message = await self.api_client.login()
            embed = self.build_status_embed("🔑 Login Realizado", f"{message}", 0x2ecc71, ctx)  # Verde
            await ctx.send(embed=embed)
        except ApiError as e:
            embed = self.build_status_embed("❌ Erro no Login", e.detail, 0xe74c3c, ctx)  # Vermelho
            await ctx.send(embed=embed)
        except Exception as e:
            embed = self.build_status_embed("❌ Erro inesperado", str(e), 0xe74c3c, ctx)
            await ctx.send(embed=embed)

    @commands.command(name="refresh-token")
    @commands.check(is_admin_or_authorized)
    async def refresh_token(self, ctx):
        """Comando para o refresh manual."""
        try:
            message = await self.api_client.refresh_token_manual()
            embed = self.build_status_embed("🔄 Token Atualizado", f"{message}", 0x3498db, ctx)  # Azul
            await ctx.send(embed=embed)
        except ApiError as e:
            embed = self.build_status_embed("❌ Erro no Refresh", e.detail, 0xe74c3c, ctx)
            await ctx.send(embed=embed)
        except Exception as e:
            embed = self.build_status_embed("❌ Erro inesperado", str(e), 0xe74c3c, ctx)
            await ctx.send(embed=embed)

    @commands.command(name="logout")
    @commands.check(is_admin_or_authorized)
    async def logout(self, ctx):
        """Comando para fazer logout."""
        try:
            message = await self.api_client.logout()
            embed = self.build_status_embed("🚪 Logout Realizado", f"{message}", 0xf39c12, ctx)  # Laranja
            await ctx.send(embed=embed)
        except ApiError as e:
            embed = self.build_status_embed("❌ Erro no Logout", e.detail, 0xe74c3c, ctx)
            await ctx.send(embed=embed)
        except Exception as e:
            embed = self.build_status_embed("❌ Erro inesperado", str(e), 0xe74c3c, ctx)
            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Admin(bot))