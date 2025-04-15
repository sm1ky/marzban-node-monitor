from dotenv import load_dotenv
import os

load_dotenv()


class Config:
    MARZBAN_BASE_URL = os.getenv("MARZBAN_BASE_URL", "https://example.com/api").strip()
    MARZBAN_USERNAME = os.getenv("MARZBAN_USERNAME", "admin").strip()
    MARZBAN_PASSWORD = os.getenv("MARZBAN_PASSWORD", "PASSWORD").strip()
    TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "TOKEN").strip()
    TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "-1002178231").strip()
    TELEGRAM_THREAD_CHAT_ID = os.getenv("TELEGRAM_THREAD_CHAT_ID", "").strip()
    REDIS_HOST = os.getenv("REDIS_HOST", "redis").strip()
    REDIS_PORT = int(os.getenv("REDIS_PORT", 6379).strip())
    REDIS_DB = int(os.getenv("REDIS_DB", 1).strip())
    TELEGRAM_LOGS = os.getenv("TELEGRAM_LOGS", "true").strip()
    TELEGRAM_LOGS = True if TELEGRAM_LOGS.lower() == "true" else False
    REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", "PASSWORD").strip()
    LOG_LEVEL = os.getenv("LOG_LEVEL", "DEFAULT").strip().upper()
    VALID_LOG_LEVELS = {"DEBUG", "INFO"}

    if LOG_LEVEL not in VALID_LOG_LEVELS:
        LOG_LEVEL = "INFO"


class Responses:
    LANG = os.getenv("LANG", "ru")

    MESSAGES = {
        "ru": {
            "MONITOR_START": (
                "✅ <b>Мониторинг начался.</b>\n\n"
                "<i>Проверка узлов запущена...</i>\n"
                "<code>----------------------------------------</code>\n\n"
            ),
            "SUCCESS_MONITOR_START": (
                "✅ <b>Мониторинг начался.</b>\n\n"
                "<b>Общее количество узлов:</b> {node_count}\n\n"
                "<i>Проверка узлов запущена...</i>\n"
                "<code>----------------------------------------</code>\n\n"
            ),
            "SUCCESS_NODE_RECONNECTED": (
                "🟢 <b>Узел восстановлен</b>\n\n"
                "<b>Узел:</b> <code>{node_name}</code>\n"
                "<b>IP:</b> <code>{node_ip}</code>\n\n"
                "<code>----------------------------------------</code>\n"
                "<b>Время восстановления:</b> {timestamp}\n"
                "<b>Время простоя:</b> {downtime_minutes} минут\n"
                "<code>----------------------------------------</code>\n\n"
            ),
            "SUCCESS_NODE_RECONNECTED_AFTER_ATTEMPTS": (
                "🟢 <b>Узел восстановлен после нескольких попыток</b>\n\n"
                "<b>Узел:</b> <code>{node_name}</code>\n"
                "<b>IP:</b> <code>{node_ip}</code>\n\n"
                "<code>----------------------------------------</code>\n"
                "<b>Время восстановления:</b> {timestamp}\n"
                "<b>Время простоя:</b> {downtime_minutes} минут\n"
                "<b>Попытки переподключения:</b> {attempts}\n"
                "<code>----------------------------------------</code>\n\n"
            ),
            "ERROR_NODE_DISCONNECTED": (
                "🔴 <b>[ALERT]</b>\n\n"
                "<b>Узел:</b> <code>{node_name}</code>\n"
                "<b>IP:</b> <code>{node_ip}</code>\n\n"
                "<code>----------------------------------------</code>\n"
                "<b>Ошибка:</b> <code>{error_message}</code>\n"
                "<b>Попытка переподключения:</b> {timestamp}\n"
                "<code>----------------------------------------</code>\n\n"
            ),
            "ERROR_NODE_RECONNECT_ATTEMPT": (
                "⚠️ <b>[Попытка {attempt}]</b>\n\n"
                "<b>Узел:</b> <code>{node_name}</code>\n"
                "<b>IP:</b> <code>{node_ip}</code>\n\n"
                "<code>----------------------------------------</code>\n"
                "<b>Попытка переподключения:</b> {attempt}/{max_checks}\n"
                "<b>Время:</b> {timestamp}\n"
                "<code>----------------------------------------</code>\n\n"
            ),
            "ERROR_NODE_RECONNECT_FAILED": (
                "🔴 <b>[CRITICAL]</b>\n\n"
                "<b>Узел:</b> <code>{node_name}</code>\n"
                "<b>IP:</b> <code>{node_ip}</code>\n\n"
                "<code>----------------------------------------</code>\n"
                "Не удалось переподключить узел после {attempts} попыток.\n"
                "<b>Ошибка:</b> <code>{error_message}</code>\n"
                "<b>Время:</b> {timestamp}\n"
                "<code>----------------------------------------</code>\n\n"
            ),
            "ERROR_MONITOR_FAILURE": (
                "❗ <b>[ERROR]</b>\n\n"
                "<b>Произошла ошибка при мониторинге узлов.</b>\n\n"
                "<code>----------------------------------------</code>\n"
                "<b>Ошибка:</b> <code>{error_message}</code>\n"
                "<b>Время:</b> {timestamp}\n"
                "<code>----------------------------------------</code>\n\n"
            ),
        },
        "en": {
            "MONITOR_START": (
                "✅ <b>Monitoring started.</b>\n\n"
                "<i>Node checking started...</i>\n"
                "<code>----------------------------------------</code>\n\n"
            ),
            "SUCCESS_MONITOR_START": (
                "✅ <b>Monitoring started.</b>\n\n"
                "<b>Total nodes:</b> {node_count}\n\n"
                "<i>Node checking started...</i>\n"
                "<code>----------------------------------------</code>\n\n"
            ),
            "SUCCESS_NODE_RECONNECTED": (
                "🟢 <b>Node reconnected</b>\n\n"
                "<b>Node:</b> <code>{node_name}</code>\n"
                "<b>IP:</b> <code>{node_ip}</code>\n\n"
                "<code>----------------------------------------</code>\n"
                "<b>Reconnected at:</b> {timestamp}\n"
                "<b>Downtime:</b> {downtime_minutes} minutes\n"
                "<code>----------------------------------------</code>\n\n"
            ),
            "SUCCESS_NODE_RECONNECTED_AFTER_ATTEMPTS": (
                "🟢 <b>Node reconnected after several attempts</b>\n\n"
                "<b>Node:</b> <code>{node_name}</code>\n"
                "<b>IP:</b> <code>{node_ip}</code>\n\n"
                "<code>----------------------------------------</code>\n"
                "<b>Reconnected at:</b> {timestamp}\n"
                "<b>Downtime:</b> {downtime_minutes} minutes\n"
                "<b>Reconnect attempts:</b> {attempts}\n"
                "<code>----------------------------------------</code>\n\n"
            ),
            "ERROR_NODE_DISCONNECTED": (
                "🔴 <b>[ALERT]</b>\n\n"
                "<b>Node:</b> <code>{node_name}</code>\n"
                "<b>IP:</b> <code>{node_ip}</code>\n\n"
                "<code>----------------------------------------</code>\n"
                "<b>Error:</b> <code>{error_message}</code>\n"
                "<b>Reconnect attempt:</b> {timestamp}\n"
                "<code>----------------------------------------</code>\n\n"
            ),
            "ERROR_NODE_RECONNECT_ATTEMPT": (
                "⚠️ <b>[Attempt {attempt}]</b>\n\n"
                "<b>Node:</b> <code>{node_name}</code>\n"
                "<b>IP:</b> <code>{node_ip}</code>\n\n"
                "<code>----------------------------------------</code>\n"
                "<b>Reconnect attempt:</b> {attempt}/{max_checks}\n"
                "<b>Time:</b> {timestamp}\n"
                "<code>----------------------------------------</code>\n\n"
            ),
            "ERROR_NODE_RECONNECT_FAILED": (
                "🔴 <b>[CRITICAL]</b>\n\n"
                "<b>Node:</b> <code>{node_name}</code>\n"
                "<b>IP:</b> <code>{node_ip}</code>\n\n"
                "<code>----------------------------------------</code>\n"
                "Failed to reconnect the node after {attempts} attempts.\n"
                "<b>Error:</b> <code>{error_message}</code>\n"
                "<b>Time:</b> {timestamp}\n"
                "<code>----------------------------------------</code>\n\n"
            ),
            "ERROR_MONITOR_FAILURE": (
                "❗ <b>[ERROR]</b>\n\n"
                "<b>An error occurred during node monitoring.</b>\n\n"
                "<code>----------------------------------------</code>\n"
                "<b>Error:</b> <code>{error_message}</code>\n"
                "<b>Time:</b> {timestamp}\n"
                "<code>----------------------------------------</code>\n\n"
            ),
        },
    }

    @classmethod
    def get_message(cls, message_key, **kwargs):
        """Возвращает сообщение на текущем языке с подстановкой переменных."""
        message_template = cls.MESSAGES[cls.LANG].get(message_key)
        if message_template:
            return message_template.format(**kwargs)
        return f"Message with key '{message_key}' not found."
