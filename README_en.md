
# Marzban Node Monitor

## Description

**Marzban Node Monitor** is a microservice for automatically monitoring and managing the status of nodes in the Marzban system. It regularly checks the status of all nodes, restarts them if any issues are detected, and sends notifications to Telegram, allowing for timely responses to any system failures.

## Key Features

- **Node Monitoring:** Regular checks of all nodes using the Marzban API.
- **Node Restart:** Automatic restart of nodes that are not functioning correctly.
- **Telegram Notifications:** Sends notifications to Telegram about any changes in the status of nodes.

## Technologies Used

- **Python 3.11** — main programming language.
- **HTTPX** — library for making HTTP requests.
- **Docker** — used for containerization and easy deployment of the microservice.
- **Redis** — used for caching data.
- **dotenv** — for secure storage of sensitive information (tokens, passwords, etc.).

## Installation and Usage

### Docker Installation

To install Docker, run the following command:

```bash
curl -fsSL https://get.docker.com -o get-docker.sh && sh get-docker.sh
```

### Project Setup

1. Clone the repository:
    ```bash
    git clone https://github.com/sm1ky/marzban-node-monitor.git
    cd marzban-node-monitor
    ```

2. Create a `.env` file and add the following environment variables:

    ```env
    MARZBAN_BASE_URL=https://your-marzban-instance.com/api
    MARZBAN_USERNAME=your_username
    MARZBAN_PASSWORD=your_password
    TELEGRAM_TOKEN=your_telegram_bot_token
    TELEGRAM_CHAT_ID=your_telegram_chat_id
    TELEGRAM_THREAD_CHAT_ID=
    REDIS_HOST=redis
    REDIS_PORT=6379
    REDIS_DB=1
    REDIS_PASSWORD=PASSWORD
    LOG_LEVEL=DEFAULT
    LANG=en
    ```
    
### Start Docker Containers

To start the microservice and Redis, run the following command:

```bash
docker compose up -d
```

Docker will automatically create the `monitor_network` if it hasn't been created already and will start the containers within this network.

### Updating the Project

To update the project after changes in the repository, follow these steps:

1. Go to the project directory:
    ```bash
    cd marzban-node-monitor
    ```

2. Fetch the latest changes from the repository:
    ```bash
    git pull origin production
    ```

3. Restart the containers without rebuilding images:
    ```bash
    docker compose up -d
    ```

## License

This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for details.

## Developer Contact

- **Name:** Artem
- **Contact:** [dev@sm1ky.com](mailto:dev@sm1ky.com) | [Telegram](https://t.me/forests_vpn)
