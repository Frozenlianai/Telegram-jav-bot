# tg-search-bot (中文文档)

**一个用于查询与收藏演员和影片的机器人, 可自动保存磁链到 Pikpak。**

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
-   **/rank**: 获取 DMM 女优排行榜
-   **/stats**: 查看机器人统计信息（仅限管理员）
-   **/record**: 获取收藏记录文件(`record.json`)
-   **/star `[演员名称]`**: 搜索指定演员
-   **/av `[番号]`**: 搜索指定番号
-   **内联 an-chaxun `[查询词]`**: 内联查询

## TODO 

- [x] 英文版本
- [ ] 微服务架构

## 使用教程

### 1. 克隆项目

```bash
git clone https://github.com/akynazh/tg-jav-bot.git
cd tg-jav-bot
```

### 2. 配置机器人

复制环境变量示例文件，并填入你的配置：

```bash
cp .env.example .env
```

接着，编辑 `.env` 文件，填入你的 Telegram Bot Token, Chat ID 等信息。

### 3. 通过 Docker 运行 (推荐)

```bash
docker-compose up -d --build
```

### 4. 手动运行 (开发)

确保你已安装 Python >= 3.7 并已启动 Redis 服务。

```bash
pip install -r requirements.txt && python main.py
```

### 更新机器人

拉取最新代码后，重新构建并运行 Docker 即可：

```bash
docker-compose down && docker-compose up -d --build
``` 