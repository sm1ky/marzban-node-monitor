import time
from datetime import datetime
from .telegram_notifier import TelegramNotifier
from .marzban_api import MarzbanAPI
from .config import Config, Responses
import redis
import logging


class NodeMonitor:
    def __init__(self):
        self.api = MarzbanAPI()
        self.notifier = TelegramNotifier()
        self.redis = redis.Redis(
            host=Config.REDIS_HOST,
            port=Config.REDIS_PORT,
            db=Config.REDIS_DB,
            password=Config.REDIS_PASSWORD,
        )
        self.node_status_key_prefix = "node_status:"
        self.node_disconnect_time_prefix = "node_disconnect_time:"

    def get_node_status_key(self, node_id):
        return f"{self.node_status_key_prefix}{node_id}"

    def get_node_disconnect_time_key(self, node_id):
        return f"{self.node_disconnect_time_prefix}{node_id}"

    def log_node_info(self, node):
        logging.info(f"--- Узел: {node.get('name', 'Неизвестный узел')} ---")
        logging.info(f"ID: {node.get('id', 'Неизвестно')}")
        logging.info(f"Адрес: {node.get('address', 'IP не указан')}")
        logging.info(f"Порт: {node.get('port', 'Неизвестно')}")
        logging.info(f"Статус: {node.get('status', 'Неизвестно')}")
        logging.info(f"Сообщение: {node.get('message', 'Ошибка не указана')}")

    def monitor(self):
        self.notifier.send_message(
            Responses.get_message("MONITOR_START"),
            parse_mode="HTML",
        )
        while True:
            try:
                logging.info("Начало мониторинга узлов...")
                nodes = self.api.get_nodes()
                logging.info(f"Получено {len(nodes)} узлов для мониторинга.")

                if Config.LOG_LEVEL == "DEBUG":
                    self.notifier.send_message(
                        Responses.get_message(
                            "SUCCESS_MONITOR_START", node_count=len(nodes)
                        ),
                        parse_mode="HTML",
                    )

                for node in nodes:
                    self.log_node_info(node)

                    node_id = node["id"]
                    node_name = node["name"]
                    node_ip = node.get("address", "IP не указан")
                    node_message = node.get("message", "Ошибка не указана")
                    node_redis_key = self.get_node_status_key(node_id)
                    node_disconnect_time_key = self.get_node_disconnect_time_key(
                        node_id
                    )

                    node_status = self.api.get_node(node_id)
                    current_status = node_status.get("status", "unknown")
                    logging.info(f"Статус узла {node_name}: {current_status}")

                    if (
                        self.redis.get(node_redis_key) == b"disconnected"
                        and current_status == "connected"
                    ):
                        disconnect_time = self.redis.get(node_disconnect_time_key)
                        if disconnect_time:
                            disconnect_time = float(disconnect_time)
                            reconnect_time = time.time()
                            downtime = reconnect_time - disconnect_time
                            downtime_minutes = round(downtime / 60, 2)
                            timestamp_reconnect = datetime.now().strftime(
                                "%Y-%m-%d %H:%M:%S"
                            )
                            logging.info(
                                f"Узел {node_name} восстановлен через "
                                f"{downtime_minutes} минут."
                            )
                            self.notifier.send_message(
                                Responses.get_message(
                                    "SUCCESS_NODE_RECONNECTED",
                                    node_name=node_name,
                                    node_ip=node_ip,
                                    timestamp=timestamp_reconnect,
                                    downtime_minutes=downtime_minutes,
                                ),
                                parse_mode="HTML",
                            )
                        self.redis.delete(node_redis_key)
                        self.redis.delete(node_disconnect_time_key)

                    if current_status not in ["connected", "disabled"]:
                        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        logging.warning(
                            f"Узел {node_name} ({node_ip}) отключен. "
                            f"Попытка переподключения в {timestamp}..."
                        )

                        if self.redis.get(node_redis_key) != b"disconnected":
                            self.notifier.send_message(
                                Responses.get_message(
                                    "ERROR_NODE_DISCONNECTED",
                                    node_name=node_name,
                                    node_ip=node_ip,
                                    error_message=node_message,
                                    timestamp=timestamp,
                                ),
                                parse_mode="HTML",
                            )
                            self.redis.set(node_redis_key, "disconnected")
                            self.redis.set(node_disconnect_time_key, time.time())

                        self.api.reconnect_node(node_id)
                        time.sleep(10)

                        max_checks = 3
                        attempts = 0

                        for i in range(max_checks):
                            attempts += 1
                            node_status = self.api.get_node(node_id)
                            if node_status["status"] == "connected":
                                timestamp_reconnect = datetime.now().strftime(
                                    "%Y-%m-%d %H:%M:%S"
                                )
                                disconnect_time = self.redis.get(
                                    node_disconnect_time_key
                                )
                                if disconnect_time:
                                    disconnect_time = float(disconnect_time)
                                    reconnect_time = time.time()
                                    downtime = reconnect_time - disconnect_time
                                    downtime_minutes = round(downtime / 60, 2)
                                else:
                                    downtime_minutes = 0

                                logging.info(
                                    f"Узел {node_name} восстановлен в "
                                    f"{timestamp_reconnect} после {attempts} попыток."
                                )
                                self.notifier.send_message(
                                    Responses.get_message(
                                        "SUCCESS_NODE_RECONNECTED_AFTER_ATTEMPTS",
                                        node_name=node_name,
                                        node_ip=node_ip,
                                        timestamp=timestamp_reconnect,
                                        attempts=attempts,
                                        downtime_minutes=downtime_minutes,
                                    ),
                                    parse_mode="HTML",
                                )
                                self.redis.delete(node_redis_key)
                                self.redis.delete(node_disconnect_time_key)
                                break
                            else:
                                timestamp_attempt = datetime.now().strftime(
                                    "%Y-%m-%d %H:%M:%S"
                                )
                                logging.warning(
                                    f"Узел {node_name} ({node_ip}) не переподключен. "
                                    f"Попытка {i + 1}/{max_checks}. "
                                    f"Время: {timestamp_attempt}"
                                )
                                if Config.LOG_LEVEL == "DEBUG":
                                    self.notifier.send_message(
                                        Responses.get_message(
                                            "ERROR_NODE_RECONNECT_ATTEMPT",
                                            node_name=node_name,
                                            node_ip=node_ip,
                                            attempt=i + 1,
                                            max_checks=max_checks,
                                            timestamp=timestamp_attempt,
                                        ),
                                        parse_mode="HTML",
                                    )
                                time.sleep(5)

                        if (
                            node_status["status"] != "connected"
                            and self.redis.get(node_redis_key) != b"disconnected"
                        ):
                            timestamp_failure = datetime.now().strftime(
                                "%Y-%m-%d %H:%M:%S"
                            )
                            logging.error(
                                f"Не удалось переподключить узел {node_name} "
                                f"в {timestamp_failure}. Попытки: {max_checks}"
                            )
                            self.notifier.send_message(
                                Responses.get_message(
                                    "ERROR_NODE_RECONNECT_FAILED",
                                    node_name=node_name,
                                    node_ip=node_ip,
                                    error_message=node_message,
                                    attempts=max_checks,
                                    timestamp=timestamp_failure,
                                ),
                                parse_mode="HTML",
                            )
                            self.redis.set(node_redis_key, "disconnected")

                time.sleep(30)

            except Exception as e:
                timestamp_error = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                logging.error(f"Ошибка при мониторинге узлов: {e} в {timestamp_error}")
                self.notifier.send_message(
                    Responses.get_message(
                        "ERROR_MONITOR_FAILURE",
                        error_message=str(e),
                        timestamp=timestamp_error,
                    ),
                    parse_mode="HTML",
                )
