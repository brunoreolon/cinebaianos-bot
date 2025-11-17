from discord.ext import commands
from discord import Embed

from src.bot.utils.date_utils import DateUtils


class Slash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="ping", description="Teste ping")
    async def ping(self, ctx: commands.Context):
        # Calcula a latência aproximada do bot
        latencia_ms = round(self.bot.latency * 1000)  # em milissegundos

        embed = Embed(
            title="🏓 Pong!",
            description=f"Estou online e respondendo!",
            color=0x1abc9c  # verde água
        )
        embed.add_field(name="📶 Latência", value=f"{latencia_ms} ms", inline=True)
        embed.add_field(name="💻 Status", value="Online ✅", inline=True)
        embed.set_footer(text=f"Consultado por {ctx.author.display_name} • {DateUtils.now_br_format()}")

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Slash(bot))