# -*- coding: UTF-8 -*-
import jvav
import telebot
from telebot import apihelper
from logger import Logger
from config import BotConfig
from database import BotFileDb, BotCacheDb
from utils.constants import PATH_LOG_FILE, PATH_RECORD_FILE

# 此处仅保留核心对象的初始化，作为全局上下文
# 后续可考虑用依赖注入框架或上下文对象进一步优化

LOG = Logger(path_log_file=PATH_LOG_FILE).logger
BOT_CFG = BotConfig()

# 检查 token 是否存在
if not BOT_CFG.tg_bot_token:
    LOG.error("TG_BOT_TOKEN 未配置，机器人无法初始化。")
    exit(1)

apihelper.proxy = BOT_CFG.proxy_json
BOT = telebot.TeleBot(BOT_CFG.tg_bot_token)
BOT_DB = BotFileDb(PATH_RECORD_FILE)
BOT_CACHE_DB = BotCacheDb(
    host=BOT_CFG.redis_host, port=int(BOT_CFG.redis_port), use_cache=BOT_CFG.use_cache
)

# 初始化所有 API 工具
BASE_UTIL = jvav.BaseUtil(BOT_CFG.proxy_addr)
DMM_UTIL = jvav.DmmUtil(BOT_CFG.proxy_addr_dmm)
JAVBUS_UTIL = jvav.JavBusUtil(BOT_CFG.proxy_addr)
JAVLIB_UTIL = jvav.JavLibUtil(BOT_CFG.proxy_addr)
SUKEBEI_UTIL = jvav.SukebeiUtil(BOT_CFG.proxy_addr)
TRANS_UTIL = jvav.TransUtil(BOT_CFG.proxy_addr)
WIKI_UTIL = jvav.WikiUtil(BOT_CFG.proxy_addr)
AVGLE_UTIL = jvav.AvgleUtil(BOT_CFG.proxy_addr)
