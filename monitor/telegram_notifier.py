import httpx
from .config import Config


class TelegramNotifier:
    def __init__(self):
        self.token = Config.TELEGRAM_TOKEN
        self.chat_id = Config.TELEGRAM_CHAT_ID
        self.api_url = f"https://api.telegram.org/bot{self.token}/sendMessage"

    def send_message(self, message, parse_mode: str = "HTML"):
        data = {"chat_id": self.chat_id, "text": message, "parse_mode": parse_mode}
        try:
            httpx.post(self.api_url, data=data)
        except httpx.HTTPError as e:
            print(f"Failed to send message to Telegram: {e}")
