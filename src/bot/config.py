import os

from dotenv import load_dotenv

load_dotenv()

class Config:
    BOT_USERNAME = os.getenv("BOT_USERNAME")
    BOT_PASSWORD = os.getenv("BOT_PASSWORD")
    API_BASE_URL = os.getenv("API_BASE_URL")
    DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
    AUTHORIZED_DISCORD_IDS = list(map(int, os.getenv("AUTHORIZED_DISCORD_IDS", "").split(",")))
