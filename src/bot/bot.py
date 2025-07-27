from dotenv import load_dotenv

from src.bot.di.connection_factory import get_connection_provider

load_dotenv()

import discord
import os
import logging
import asyncio

from discord.ext import commands

from src.bot.di.schemas_factory import get_schemas_repository

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    logging.info(f"✅ Bot conectado como {bot.user}")
    try:
        synced = await bot.tree.sync()
        logging.info(f"🔄 Comandos de barra sincronizados: {len(synced)}")
    except Exception as e:
        logging.error(f"Erro ao sincronizar comandos de barra: {e}")

async def main():
    conn_provider = get_connection_provider()
    bot.conn_provider = conn_provider

    schema_repo = get_schemas_repository(conn_provider)
    schema_repo.criar_tabelas()

    await bot.load_extension("src.bot.cogs.filmes")
    await bot.load_extension("src.bot.cogs.votos")
    await bot.load_extension("src.bot.cogs.rankings")
    await bot.load_extension("src.bot.cogs.generos")
    await bot.load_extension("src.bot.cogs.usuarios")
    await bot.load_extension("src.bot.cogs.sincronizacao")
    await bot.load_extension("src.bot.cogs.links")
    await bot.load_extension("src.bot.cogs.geral")
    await bot.load_extension("src.bot.cogs.slash")

    await bot.start(TOKEN)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot parado pelo usuário.")