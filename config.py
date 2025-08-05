# -*- coding: UTF-8 -*-
import yaml
import logging
import os
from utils.constants import PATH_CONFIG_FILE

LOG = logging.getLogger(__name__)


class BotConfig:
    def __init__(self):
        """
        Initializes the bot configuration by reading from a YAML file
        and allowing overrides from environment variables.
        """
        config = {}
        try:
            if os.path.exists(PATH_CONFIG_FILE):
                with open(PATH_CONFIG_FILE, "r", encoding="utf8") as f:
                    config = yaml.safe_load(f) or {}
        except Exception as e:
            LOG.error(f"读取配置文件 {PATH_CONFIG_FILE} 出错: {e}")

        # TG Configs
        self.tg_chat_id = os.getenv("TG_CHAT_ID") or str(config.get("tg_chat_id", ""))
        self.tg_bot_token = os.getenv("TG_BOT_TOKEN") or str(config.get("tg_bot_token", ""))
        self.tg_api_id = os.getenv("TG_API_ID") or str(config.get("tg_api_id", ""))
        self.tg_api_hash = os.getenv("TG_API_HASH") or str(config.get("tg_api_hash", ""))

        # Proxy Configs
        self.use_proxy = str(config.get("use_proxy", "0"))
        self.use_proxy_dmm = str(config.get("use_proxy_dmm", "0"))
        self.proxy_addr = os.getenv("PROXY_ADDR") or str(config.get("proxy_addr", ""))
        
        # Pikpak Configs
        self.use_pikpak = str(config.get("use_pikpak", "0"))

        # Cache Configs
        self.use_cache = str(config.get("use_cache", "0"))
        self.redis_host = os.getenv("REDIS_HOST") or str(config.get("redis_host", "localhost"))
        self.redis_port = str(config.get("redis_port", "6379"))

        # Processed proxy settings
        self.proxy_addr_dmm = ""
        self.proxy_json = {}
        self.proxy_json_pikpak = {}
        
        if self.use_proxy == "1" and self.proxy_addr:
            self.proxy_json = {"http": self.proxy_addr, "https": self.proxy_addr}
            self.proxy_addr_dmm = self.proxy_addr
            try:
                # expecting http://user:pass@host:port or socks5://user:pass@host:port
                parts = self.proxy_addr.replace("://", " ").replace(":", " ").replace("@", " ").split()
                if len(parts) == 4: # with auth
                    scheme, user, password, host, port = parts[0], parts[1], parts[2], parts[3], parts[4]
                elif len(parts) == 3: # no auth
                    scheme, host, port = parts[0], parts[1], parts[2]
                else: # simple host:port
                    raise ValueError("Invalid proxy format")
                
                self.proxy_json_pikpak = {
                    "scheme": scheme,
                    "hostname": host,
                    "port": int(port),
                }
                if 'user' in locals() and 'password' in locals():
                    self.proxy_json_pikpak.update({"username":user, "password":password})
                LOG.info(f'设置全局代理: "{self.proxy_addr}"')
            except Exception as e:
                LOG.error(f"解析 PikPak 代理地址出错: {e}, 格式应为 'scheme://user:pass@host:port' 或 'scheme://host:port'")

        elif self.use_proxy_dmm == "1" and self.proxy_addr:
            self.proxy_addr_dmm = self.proxy_addr
            LOG.info(f'设置 DMM 代理: "{self.proxy_addr_dmm}"')
