import logging as log
import os
import time
import telebot
from dotenv import load_dotenv
from src.model.handlers.command_handler import command_handlers
from src.model.handlers.link_youtube_handler import link_youtube_handler
from src.model.handlers.callback_handler import callback_handler

load_dotenv()

YOUTUBE_REGEX = r"(https?://)?(www\.)?(youtube\.com|youtu\.be)/\S+"

def bot():
    print('bot chamado')
    log.info('bot chamado')
    
    bot = telebot.TeleBot(os.getenv("TOKEN_BOT"))
    
    bot.remove_webhook()
    time.sleep(1)
    
    bot.user_data = {}
    
    command_handlers(bot)
    link_youtube_handler(bot)
    callback_handler(bot)
    
    bot.infinity_polling(timeout=120, long_polling_timeout=120)

if __name__ == '__main__':
    bot()