import time
import logging
from .marzban_api import MarzbanAPI
from .telegram_notifier import TelegramNotifier

# Настройка логирования для вывода в консоль
logging.basicConfig(level=logging.INFO)


class NodeMonitor:
    def __init__(self):
        self.api = MarzbanAPI()
        self.notifier = TelegramNotifier()

    def monitor(self):
        while True:
            try:
                print("Начало мониторинга...")
                nodes = self.api.get_nodes()
                print(f"Получено {len(nodes)} узлов для мониторинга.")
                for node in nodes:
                    node_id = node['id']
                    node_name = node['name']

                    print(f"Проверка узла: {node_name}")
                    node_status = self.api.get_node(node_id)
                    print(f"Статус узла {node_name}: {node_status['status']}")

                    if node_status['status'] not in ['connected', 'disabled']:
                        print(
                            f"Узел {node_name} отключен. Попытка переподключения...")
                        self.notifier.send_message(
                            f"Узел {node_name} отключен. Попытка переподключения...")
                        self.api.reconnect_node(node_id)
                        time.sleep(10)

                        max_checks = 3
                        for i in range(max_checks):
                            node_status = self.api.get_node(node_id)
                            if node_status['status'] == 'connected':
                                print(f"Узел {node_name} переподключен.")
                                self.notifier.send_message(
                                    f"Node {node_name} is back online."
                                )
                                break
                            else:
                                print(
                                    f"Узел {node_name} еще не переподключен. "
                                    f"Попытка {i + 1}/{max_checks}."
                                )
                                time.sleep(5)

                        if node_status['status'] != 'connected':
                            print(
                                f"Не удалось переподключить узел {node_name}.")
                            self.notifier.send_message(
                                f"Не удалось переподключить узел {node_name}."
                            )
                time.sleep(30)
            except Exception as e:
                print(f"Ошибка при мониторинге узлов: {e}")
