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

## Commands

-   /help or /start: Show help message with inline buttons
-   /rank: Get DMM actress rankings
-   /stats: View bot statistics (admin only)
-   /record: Get collection record file (`record.json`)
-   /star `[actress name]`: Search for specific actress
-   /av `[movie code]`: Search for specific movie
-   Inline an-chaxun `[query]`: Inline query

## TODO

-   [x] English version
-   [ ] Microservices architecture

## Prerequisites

Before installing the bot, make sure you have:

- Python 3.7+ (for manual installation)
- Docker & Docker Compose (for Docker installation)
- Redis (included in Docker setup, or install separately for manual setup)
- Telegram Bot Token (get from [@BotFather](https://t.me/BotFather))
- Telegram Chat ID (your personal chat ID or admin group ID)

## Installation

### Method 1: Docker Installation (Recommended)

#### 1. Clone the project

```bash
git clone https://github.com/akynazh/tg-jav-bot.git
cd tg-jav-bot
```

#### 2. Configure Environment Variables

Create a `.env` file in the project root:

```bash
# Create .env file
touch .env
```

Edit `.env` with your configuration:

```env
# Telegram Bot Configuration
TG_BOT_TOKEN=your_bot_token_here
TG_CHAT_ID=your_chat_id_here
TG_API_ID=your_api_id_here
TG_API_HASH=your_api_hash_here

# Proxy Configuration (Optional)
USE_PROXY=0
USE_PROXY_DMM=0
PROXY_ADDR=http://user:pass@host:port

# Pikpak Configuration (Optional)
USE_PIKPAK=0

# Cache Configuration
USE_CACHE=1
REDIS_HOST=redis
REDIS_PORT=6379
```

#### 3. Run with Docker Compose

```bash
# Build and start all services
docker-compose up -d --build

# Check logs
docker-compose logs -f tg-jav-bot

# Stop services
docker-compose down
```

### Method 2: Manual Installation

#### 1. Clone the project

```bash
git clone https://github.com/akynazh/tg-jav-bot.git
cd tg-jav-bot
```

#### 2. Install Python dependencies

```bash
# Install Python 3.7+ if not already installed
# Ubuntu/Debian:
sudo apt update && sudo apt install python3 python3-pip python3-venv

# macOS:
brew install python3

# Windows:
# Download from https://www.python.org/downloads/

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# Linux/macOS:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

#### 3. Install and configure Redis

Ubuntu/Debian:
```bash
sudo apt install redis-server
sudo systemctl start redis-server
sudo systemctl enable redis-server
```

macOS:
```bash
brew install redis
brew services start redis
```

Windows:
```bash
# Download Redis for Windows from https://github.com/microsoftarchive/redis/releases
# Or use WSL2 with Ubuntu
```

#### 4. Configure Environment Variables

Create a `.env` file or set environment variables:

```bash
# Option 1: Create .env file (same as Docker method)
touch .env
# Edit .env with your configuration

# Option 2: Set environment variables
export TG_BOT_TOKEN="your_bot_token_here"
export TG_CHAT_ID="your_chat_id_here"
export TG_API_ID="your_api_id_here"
export TG_API_HASH="your_api_hash_here"
export USE_CACHE="1"
export REDIS_HOST="localhost"
export REDIS_PORT="6379"
```

#### 5. Run the bot

```bash
# Make sure virtual environment is activated
python main.py
```

## Configuration Details

### Required Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `TG_BOT_TOKEN` | Your Telegram bot token from @BotFather | `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz` |
| `TG_CHAT_ID` | Your personal chat ID or admin group ID | `123456789` |
| `TG_API_ID` | Telegram API ID (for Pyrogram) | `12345678` |
| `TG_API_HASH` | Telegram API Hash (for Pyrogram) | `abcdef1234567890abcdef1234567890` |

### Optional Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `USE_PROXY` | Enable global proxy | `0` |
| `USE_PROXY_DMM` | Enable proxy for DMM only | `0` |
| `PROXY_ADDR` | Proxy address | `` |
| `USE_PIKPAK` | Enable Pikpak integration | `0` |
| `USE_CACHE` | Enable Redis caching | `0` |
| `REDIS_HOST` | Redis host address | `localhost` |
| `REDIS_PORT` | Redis port | `6379` |

### Getting Telegram Bot Token

1. Message [@BotFather](https://t.me/BotFather) on Telegram
2. Send `/newbot`
3. Follow the instructions to create your bot
4. Copy the token provided

### Getting Telegram Chat ID

1. Message [@userinfobot](https://t.me/userinfobot) on Telegram
2. It will reply with your chat ID
3. For group chat ID, add the bot to the group and check the bot's logs

### Getting Telegram API Credentials

1. Visit [my.telegram.org](https://my.telegram.org)
2. Log in with your phone number
3. Go to "API development tools"
4. Create a new application
5. Copy the API ID and API Hash

## Updating the Bot

### Docker Method

```bash
# Pull latest changes
git pull origin main

# Rebuild and restart
docker-compose down
docker-compose up -d --build
```

### Manual Method

```bash
# Pull latest changes
git pull origin main

# Update dependencies (if needed)
pip install -r requirements.txt

# Restart the bot
# Stop current process and run again
python main.py
```

## Troubleshooting

### Common Issues

1. Bot not responding
- Check if bot token is correct
- Verify chat ID is correct
- Ensure bot has necessary permissions

2. Redis connection error
- Check if Redis is running: `redis-cli ping`
- Verify Redis host and port in configuration
- For Docker: Check if Redis container is running

3. Proxy issues
- Verify proxy format: `scheme://user:pass@host:port`
- Test proxy connectivity manually
- Check firewall settings

4. Permission denied errors
- Ensure bot has admin rights in groups
- Check file permissions for data directory

### Logs and Debugging

Docker logs:
```bash
# View bot logs
docker-compose logs -f tg-jav-bot

# View Redis logs
docker-compose logs -f redis

# View all logs
docker-compose logs -f
```

Manual installation logs:
- Check console output for error messages
- Logs are typically printed to stdout

### Performance Optimization

- Enable Redis caching for better performance
- Use proxy if accessing from restricted regions
- Consider using SSD storage for better I/O performance

## Development

### Running Tests

```bash
# Install test dependencies
pip install pytest

# Run tests
pytest tests/
```

### Code Style

```bash
# Install development dependencies
pip install autopep8 pylint

# Format code
autopep8 --in-place --recursive .

# Lint code
pylint *.py handlers/ utils/
```

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

If you encounter any issues:

1. Check the troubleshooting section above
2. Search existing issues on GitHub
3. Create a new issue with detailed information
4. Join our community discussions

## Acknowledgments

- Thanks to all contributors
- Built with [pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI)
- Redis for caching
- Docker for containerization
