from discord.ext import commands
import discord

class Slash(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="ping", description="teste")
    async def ping(self, interaction: discord.Interaction):
        await interaction.response.send_message("🏓 Pong! Estou online")

async def setup(bot):
    await bot.add_cog(Slash(bot))