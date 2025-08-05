"""
主入口文件，负责启动 bot 并注册 handler
"""

from config import BotConfig
from logger import Logger
import telebot
from telebot import types
from handlers.message import register_message_handlers
from handlers.callback import register_callback_handlers
from handlers.member import register_member_handlers
from utils.constants import BOT_CMDS, PATH_LOG_FILE, PATH_ROOT
import os

def main():
    if not os.path.exists(PATH_ROOT):
        os.makedirs(PATH_ROOT)
        
    cfg = BotConfig()
    logger = Logger(PATH_LOG_FILE).logger
    
    if not cfg.tg_bot_token:
        logger.error("TG_BOT_TOKEN 未配置，机器人无法启动。")
        return
        
    bot = telebot.TeleBot(cfg.tg_bot_token)
    bot.set_my_commands([types.BotCommand(cmd, BOT_CMDS[cmd]) for cmd in BOT_CMDS])
    register_message_handlers(bot)
    register_callback_handlers(bot)
    register_member_handlers(bot)
    
    logger.info("机器人启动中...")
    bot.polling()

if __name__ == "__main__":
    main() 