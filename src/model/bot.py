import logging as log
import os
import telebot
import re
from src.model.download import download_audio
from src.model.download import download_video
from src.model.apagar_arquivos import apagar_arquivos
from src.model.download import get_title
from src.model.download import get_thumb
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

BOT_TOKEN = '8008948209:AAGcIJmEhB81t-oKNJsljyG_4brDM5y8Ifk'

YOUTUBE_REGEX = r"(https?://)?(www\.)?(youtube\.com|youtu\.be)/\S+"

def bot():
    
    log.info('bot chamado')
    
    bot = telebot.TeleBot(BOT_TOKEN)
    
    bot.remove_webhook()
    
    @bot.message_handler(commands=['start', 'hello'])
    def send_instructions(message):
        bot.reply_to(message, "Olá eu sou um Bot de Download\n\nMe envie um link do Youtube")
    
    @bot.message_handler(func=lambda message: re.search(YOUTUBE_REGEX, message.text))
    def handle_youtube_link(message):
        try:
            log.info('usuario esta tentando fazer download')
            
            youtube_link = message.text.strip()
            
            markup = InlineKeyboardMarkup()
            option_video = InlineKeyboardButton("Video", callback_data="option_video")
            option_audio = InlineKeyboardButton("Audio", callback_data="option_audio")
            option_cancel = InlineKeyboardButton("Cancel", callback_data="option_cancel")
            markup.add(option_video)
            markup.add(option_audio)
            markup.add(option_cancel)
            
            titulo = get_title(youtube_link)
            thumb = get_thumb(youtube_link)
            
            message = bot.send_photo(message.chat.id, thumb, f'<b>{titulo}</b>\n\n<b>Choose one option</b>', reply_markup=markup, parse_mode='HTML')
            
            @bot.callback_query_handler(func=lambda call: True)
            def callback_query(call):
                if call.data == "option_video":
                    bot.send_message(message.chat.id, 'Aguardando download...')
                    
                    login = os.getlogin()
                    caminho_video = f'C:\\Users\\{login}\\Desktop\\bot_telegram_yt\\video\\{titulo}.mp4'
                    
                    download_video(youtube_link, titulo)
                    
                    if os.path.getsize(caminho_video) > 50 * 1024 * 1024:
                        bot.send_message(message.chat.id, 'Erro, este video tem um limite de 50mb')
                        
                        bot.delete_message(message.chat.id, message.message_id)
                    
                        apagar_arquivos(caminho_video)
                    else:
                        try:
                            with open(caminho_video, 'rb') as video:
                                bot.send_video(message.chat.id, video)
                                
                            bot.delete_message(message.chat.id, message.message_id)
                        
                            apagar_arquivos(caminho_video)
                        except:
                            bot.send_message(message.chat.id, 'Erro, tente Novamente')

                if call.data == "option_audio":
                    bot.send_message(message.chat.id, 'Aguardando Download...')
                    
                    login = os.getlogin()
                    path_audio = f'C:\\Users\\{login}\\Desktop\\bot_telegram_yt\\audio\\{titulo}.m4a'
                    
                    download_audio(youtube_link)
                    
                    with open(path_audio, "rb") as audio:
                        bot.send_audio(message.chat.id, audio, caption=f"<b>{titulo}</b>\n\n<b>Criador: </b><a href='https://github.com/paulowelton'>GitHub</a>", parse_mode='HTML')
                    
                    bot.delete_message(message.chat.id, message.message_id)
                    
                    apagar_arquivos(path_audio)
                                
                if call.data == "option_cancel":
                    log.info('usuario cancelou o download')
                    
                    bot.delete_message(message.chat.id, message.message_id)
                    bot.send_message(message.chat.id, 'Canceled')

        except Exception as e:
            log.error(e)
            bot.send_message(message.chat.id, "O Download falhou, tente novamente...")
            
    bot.infinity_polling()

if __name__ == '__main__':
    bot()