from discord.ext import commands

class Links(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="planilha")
    async def planilha(self, ctx):
        await ctx.send("📄 Aqui está o link da planilha de filmes:\n"
                       "🔗 https://docs.google.com/spreadsheets/d/1PWZWjoitXowKcvEfY1ULjBcufDhF46AXivVLUuDHt4Q/edit?usp=sharing")

    @commands.command(name='github')
    async def github(self, ctx):
        await ctx.send("🧠 Código-fonte disponível no GitHub:\n"
                       "Bot - https://github.com/brunoreolon/bot-discord-cinebaianos\n"
                       "API - https://github.com/brunoreolon/cinebaianos-api")

async def setup(bot):
    await bot.add_cog(Links(bot))