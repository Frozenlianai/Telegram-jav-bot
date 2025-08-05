# tg-search-bot

A Telegram bot for searching and collecting actresses and movies, with auto-saving of magnet links to Pikpak.

一个用于查询与收藏演员和影片的机器人, 可自动保存磁链到 Pikpak。

Contributions are welcome! 

[中文文档 (Chinese Documentation)](README.zh-CN.md)

## Features

-   Fetch basic movie info and magnet links - 2022/11/25
-   Proxy support - 2022/11/26
-   Filter magnet links (uncensored > hd > subtitle) - 2022/11/26
-   Auto-save best magnet link to Pikpak - 2022/12/29
-   Fetch preview and full videos - 2022/12/31
-   Fetch movie screenshots - 2023/01/01
-   Collect favorite actresses and movies - 2023/01/04
-   Docker deployment - 2023/01/08
-   Actress rankings and movie ratings - 2023/01/20
-   Random high-rated and latest movies - 2023/01/25
-   Get Chinese actress names from Wikipedia - 2023/02/18
-   Translate Japanese titles - 2023/02/18
-   Search for actresses - 2023/02/18
-   Redis caching - 2023/03/17
-   Comprehensive code refactoring and modularization - 2025/06/30
-   Enhanced configuration with `.env` and environment variables - 2025/06/30
-   Optimized Docker and Docker Compose setup - 2025/06/30
-   Added automated testing framework with Pytest - 2025/06/30
-   Added Internationalization (i18n) support - 2025/06/30
-   Added microservice skeleton with FastAPI for future expansion - 2025/06/30
-   **/rank**: 获取 DMM 女优排行榜
-   **/stats**: 查看机器人统计信息（仅限管理员）
-   **/record**: 获取收藏记录文件(`record.json`)
-   **/star `[演员名称]`**: 搜索指定演员
-   **/av `[番号]`**: 搜索指定番号
-   **Inline an-chaxun `[查询词]`**: 内联查询

## TODO

-   [x] English version
-   [ ] Microservices architecture

## Installation

### 1. Clone the project

```bash
git clone https://github.com/akynazh/tg-jav-bot.git
cd tg-jav-bot
```

### 2. Configure Environment

Copy the example environment file and fill in your details:

```bash
cp .env.example .env
```

Edit `.env` with your favorite editor. You'll need to provide your Telegram bot token, chat ID, and other settings.

### 3. Run with Docker Compose

This is the recommended way to run the bot.

```bash
docker-compose up -d --build
```

### 4. Run Manually (for development)

Ensure you have Python >= 3.7 and Redis running.

```bash
pip install -r requirements.txt
python main.py
```

## Updating the Bot

1.  Pull the latest code.
2.  Re-build and run the Docker container:

```bash
docker-compose down && docker-compose up -d --build
```

</rewritten_file>
