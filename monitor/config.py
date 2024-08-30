from dotenv import load_dotenv
import os

load_dotenv()


class Config:
    MARZBAN_BASE_URL = os.getenv("MARZBAN_BASE_URL")
    MARZBAN_USERNAME = os.getenv("MARZBAN_USERNAME")
    MARZBAN_PASSWORD = os.getenv("MARZBAN_PASSWORD")
    TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
    TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
    REDIS_HOST = os.getenv("REDIS_HOST")
    REDIS_PORT = os.getenv("REDIS_PORT")
    REDIS_DB = os.getenv("REDIS_DB")
    REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")
