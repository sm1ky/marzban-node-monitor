# Marzban Node Monitor

## Описание

**Marzban Node Monitor** — это микросервис для автоматического мониторинга и управления состоянием нод в системе Marzban. Он регулярно проверяет статус всех нод, перезапускает их при обнаружении проблем и отправляет уведомления в Telegram, что позволяет оперативно реагировать на любые сбои в работе системы.

## Основные функции

- **Мониторинг нод:** Регулярная проверка состояния всех нод с использованием API Marzban.
- **Перезапуск нод:** Автоматический перезапуск нод, которые не работают корректно.
- **Уведомления в Telegram:** Отправка уведомлений в Telegram о любых изменениях в статусе нод.

## Используемые технологии

- **Python 3.11** — основной язык программирования.
- **HTTPX** — библиотека для выполнения HTTP-запросов.
- **Docker** — для контейнеризации и удобного развертывания микросервиса.
- **dotenv** — для безопасного хранения конфиденциальных данных (токены, пароли и пр.).

## Установка и использование

1. Клонируйте репозиторий:
    ```bash
    git clone https://github.com/sm1ky/marzban-node-monitor.git
    cd marzban-node-monitor
    ```

2. Создайте файл `.env` и добавьте в него следующие переменные окружения:

    ```env
    MARZBAN_BASE_URL=https://your-marzban-instance.com/api
    MARZBAN_USERNAME=your_username
    MARZBAN_PASSWORD=your_password
    TELEGRAM_TOKEN=your_telegram_bot_token
    TELEGRAM_CHAT_ID=your_telegram_chat_id
    ```

3. Запустите Docker-контейнер:
    ```bash
    docker-compose up --build
    ```

## Лицензия

Проект распространяется под лицензией MIT. Подробности смотрите в файле [LICENSE](./LICENSE).

## Разработчик

- **Имя:** Artem
- **Связь:** [dev@sm1ky.com](mailto:dev@sm1ky.com) | [Telegram](https://t.me/forests_vpn)