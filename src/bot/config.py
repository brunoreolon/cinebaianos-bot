import os

from dotenv import load_dotenv

load_dotenv()

class Config:
    BOT_API_TOKEN = os.getenv("BOT_API_TOKEN")
    BASE_URL = os.getenv("API_BASE_URL")
    TOKEN = os.getenv("DISCORD_TOKEN")
