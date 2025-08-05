# tg-search-bot (中文文档)

一个用于查询与收藏演员和影片的机器人, 可自动保存磁链到 Pikpak。

欢迎 issue 和 pr

[English Documentation](README.md)

## 功能简介

- 支持获取影片基本信息和磁链 - 2022/11/25
- 支持配置代理 - 2022/11/26
- 支持过滤磁链 (uncensored > hd > subtitle) - 2022/11/26
- 支持让机器人自动将最优磁链保存到 Pikpak - 2022/12/29
- 支持获取预览视频和完整视频 - 2022/12/31
- 支持获取影片截图 - 2023/01/01
- 支持收藏演员和影片 - 2023/01/04
- 支持通过 docker 部署 - 2023/01/08
- 支持获取演员排行榜，影片评分 - 2023/01/20
- 支持随机获取高分影片和最新影片 - 2023/01/25
- 支持通过维基百科获取演员中文名 - 2023/02/18
- 支持翻译日文标题 - 2023/02/18
- 支持搜索演员 - 2023/02/18
- 支持通过 redis 进行缓存 - 2023/03/17
- 全面代码重构与模块化 - 2025/06/30
- 优化配置系统，支持环境变量与 `.env` - 2025/06/30
- 优化 Docker 与 Docker Compose - 2025/06/30
- 集成 Pytest 自动化测试 - 2025/06/30
- 支持国际化 (i18n) - 2025/06/30
- 新增微服务架构骨架 (FastAPI) - 2025/06/30

## 命令说明

- /help 或 /start: 显示帮助信息（带内联按钮）
- /rank: 获取 DMM 女优排行榜
- /stats: 查看机器人统计信息（仅限管理员）
- /record: 获取收藏记录文件(`record.json`)
- /star `[演员名称]`: 搜索指定演员
- /av `[番号]`: 搜索指定番号
- 内联 an-chaxun `[查询词]`: 内联查询

## TODO 

- [x] 英文版本
- [ ] 微服务架构

## 环境要求

在安装机器人之前，请确保你有：

- Python 3.7+ (手动安装需要)
- Docker & Docker Compose (Docker 安装需要)
- Redis (Docker 安装已包含，手动安装需单独安装)
- Telegram Bot Token (从 [@BotFather](https://t.me/BotFather) 获取)
- Telegram Chat ID (你的个人聊天 ID 或管理员群组 ID)

## 使用教程

### 方法一：Docker 安装 (推荐)

#### 1. 克隆项目

```bash
git clone https://github.com/akynazh/tg-jav-bot.git
cd tg-jav-bot
```

#### 2. 配置环境变量

在项目根目录创建 `.env` 文件：

```bash
# 创建 .env 文件
touch .env
```

编辑 `.env` 文件，填入你的配置：

```env
# Telegram 机器人配置
TG_BOT_TOKEN=your_bot_token_here      # 你的机器人Token，向 @BotFather 申请获得
TG_CHAT_ID=your_chat_id_here          # 你的个人chat id或管理员群组id，可用 @userinfobot 获取
TG_API_ID=your_api_id_here            # Telegram API ID，需在 https://my.telegram.org 申请
TG_API_HASH=your_api_hash_here        # Telegram API Hash，需在 https://my.telegram.org 申请

# 代理配置 (可选)
USE_PROXY=0
USE_PROXY_DMM=0
PROXY_ADDR=http://user:pass@host:port

# Pikpak 配置 (可选)
USE_PIKPAK=0

# 缓存配置
USE_CACHE=1
REDIS_HOST=redis
REDIS_PORT=6379
```

#### 3. 通过 Docker 运行

```bash
# 构建并启动所有服务
docker-compose up -d --build

# 查看日志
docker-compose logs -f tg-jav-bot

# 停止服务
docker-compose down
```

### 方法二：手动安装

#### 1. 克隆项目

```bash
git clone https://github.com/akynazh/tg-jav-bot.git
cd tg-jav-bot
```

#### 2. 安装 Python 依赖

```bash
# 如果还没安装 Python 3.7+，请先安装
# Ubuntu/Debian:
sudo apt update && sudo apt install python3 python3-pip python3-venv

# macOS:
brew install python3

# Windows:
# 从 https://www.python.org/downloads/ 下载

# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境
# Linux/macOS:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt
```

#### 3. 安装并配置 Redis

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
# 从 https://github.com/microsoftarchive/redis/releases 下载 Redis for Windows
# 或使用 WSL2 + Ubuntu
```

#### 4. 配置环境变量

创建 `.env` 文件或设置环境变量：

```bash
# 选项 1: 创建 .env 文件 (与 Docker 方法相同)
touch .env
# 编辑 .env 文件填入配置

# 选项 2: 设置环境变量
export TG_BOT_TOKEN="your_bot_token_here"
export TG_CHAT_ID="your_chat_id_here"
export TG_API_ID="your_api_id_here"
export TG_API_HASH="your_api_hash_here"
export USE_CACHE="1"
export REDIS_HOST="localhost"
export REDIS_PORT="6379"
```

#### 5. 运行机器人

```bash
# 确保虚拟环境已激活
python main.py
```

## 配置详情

### 必需的环境变量

| 变量名 | 描述 | 示例 |
|--------|------|------|
| `TG_BOT_TOKEN` | 从 @BotFather 获取的机器人 token | `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz` |
| `TG_CHAT_ID` | 你的个人聊天 ID 或管理员群组 ID | `123456789` |
| `TG_API_ID` | Telegram API ID (用于 Pyrogram) | `12345678` |
| `TG_API_HASH` | Telegram API Hash (用于 Pyrogram) | `abcdef1234567890abcdef1234567890` |

### 可选的环境变量

| 变量名 | 描述 | 默认值 |
|--------|------|--------|
| `USE_PROXY` | 启用全局代理 | `0` |
| `USE_PROXY_DMM` | 仅对 DMM 启用代理 | `0` |
| `PROXY_ADDR` | 代理地址 | `` |
| `USE_PIKPAK` | 启用 Pikpak 集成 | `0` |
| `USE_CACHE` | 启用 Redis 缓存 | `0` |
| `REDIS_HOST` | Redis 主机地址 | `localhost` |
| `REDIS_PORT` | Redis 端口 | `6379` |

### 获取 Telegram Bot Token

1. 在 Telegram 中联系 [@BotFather](https://t.me/BotFather)
2. 发送 `/newbot`
3. 按照指示创建你的机器人
4. 复制提供的 token

### 获取 Telegram Chat ID

1. 在 Telegram 中联系 [@userinfobot](https://t.me/userinfobot)
2. 它会回复你的聊天 ID
3. 对于群组聊天 ID，将机器人添加到群组并查看机器人日志

### 获取 Telegram API 凭据

1. 访问 [my.telegram.org](https://my.telegram.org)
2. 使用手机号登录
3. 进入 "API development tools"
4. 创建新应用
5. 复制 API ID 和 API Hash

## 更新机器人

### Docker 方法

```bash
# 拉取最新更改
git pull origin main

# 重新构建并重启
docker-compose down
docker-compose up -d --build
```

### 手动方法

```bash
# 拉取最新更改
git pull origin main

# 更新依赖 (如需要)
pip install -r requirements.txt

# 重启机器人
# 停止当前进程并重新运行
python main.py
```

## 故障排除

### 常见问题

1. 机器人无响应
- 检查 bot token 是否正确
- 验证 chat ID 是否正确
- 确保机器人有必要的权限

2. Redis 连接错误
- 检查 Redis 是否运行: `redis-cli ping`
- 验证配置中的 Redis 主机和端口
- Docker 方式: 检查 Redis 容器是否运行

3. 代理问题
- 验证代理格式: `scheme://user:pass@host:port`
- 手动测试代理连接
- 检查防火墙设置

4. 权限被拒绝错误
- 确保机器人在群组中有管理员权限
- 检查数据目录的文件权限

### 日志和调试

Docker 日志:
```bash
# 查看机器人日志
docker-compose logs -f tg-jav-bot

# 查看 Redis 日志
docker-compose logs -f redis

# 查看所有日志
docker-compose logs -f
```

手动安装日志:
- 检查控制台输出的错误信息
- 日志通常打印到标准输出

### 性能优化

- 启用 Redis 缓存以获得更好的性能
- 如果从受限地区访问，请使用代理
- 考虑使用 SSD 存储以获得更好的 I/O 性能

## 开发

### 运行测试

```bash
# 安装测试依赖
pip install pytest

# 运行测试
pytest tests/
```

### 代码风格

```bash
# 安装开发依赖
pip install autopep8 pylint

# 格式化代码
autopep8 --in-place --recursive .

# 代码检查
pylint *.py handlers/ utils/
```

### 贡献

1. Fork 仓库
2. 创建功能分支
3. 进行更改
4. 如适用，添加测试
5. 提交 pull request

## 许可证

本项目采用 MIT 许可证 - 详情请参阅 LICENSE 文件。

## 支持

如果遇到任何问题：

1. 查看上面的故障排除部分
2. 在 GitHub 上搜索现有问题
3. 创建包含详细信息的新问题
4. 加入我们的社区讨论

## 致谢

- 感谢所有贡献者
- 基于 [pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI) 构建
- Redis 用于缓存
- Docker 用于容器化 