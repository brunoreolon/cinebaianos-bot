
import discord
import asyncio
import logging
from discord.ext import commands

from src.bot.exception.api_error import ApiError
from src.bot.config import Config
from src.bot.api_client import ApiClient

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def create_bot():
    intents = discord.Intents.default()
    intents.message_content = True
    intents.members = True

    bot = commands.Bot(command_prefix="!", intents=intents)

    @bot.event
    async def on_ready():
        logging.info(f"✅ Bot conectado como {bot.user}")
        try:
            synced = await bot.tree.sync()
            logging.info(f"✅ Comandos de barra sincronizados: {len(synced)}")
        except Exception as e:
            logging.error(f"Erro ao sincronizar comandos de barra: {e}")

    return bot

async def setup_bot():
    bot = create_bot()

    api_client = await ApiClient.create()
    bot.api_client = api_client

    # Carregar as extensões (cogs)
    cogs = [
        "src.bot.cogs.filmes",
        "src.bot.cogs.votos",
        "src.bot.cogs.rankings",
        "src.bot.cogs.generos",
        "src.bot.cogs.usuarios",
        "src.bot.cogs.sincronizacao",
        "src.bot.cogs.links",
        "src.bot.cogs.geral",
        "src.bot.cogs.slash",
    ]

    for cog in cogs:
        await bot.load_extension(cog)

    return bot

async def main():
    bot = None
    api_client = None

    try:
        bot = await setup_bot()
        api_client = bot.api_client

        await bot.start(Config.DISCORD_TOKEN)

    except ApiError as e:
        logging.error(f"❌ Erro na API: {e.title or e.code} - {e.detail}")
    except KeyboardInterrupt:
        logging.info("Bot parado pelo usuário.")
    except Exception as e:
        logging.exception(f"Erro inesperado: {e}")
    finally:
        if api_client:
            await api_client.close()

        if bot and not bot.is_closed():
            await bot.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Bot parado pelo usuário.")