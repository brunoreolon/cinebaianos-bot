from discord.ext import commands

class Slash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="ping", description="Teste ping")
    async def ping(self, ctx: commands.Context):
        await ctx.send("🏓 Pong! Estou online")

async def setup(bot):
    await bot.add_cog(Slash(bot))