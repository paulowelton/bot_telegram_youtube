import re
import logging as log
from src.model.download import get_title
from src.model.download import get_thumb
from src.model.sanitize_filename import sanitize_filename
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

YOUTUBE_REGEX = r"(https?://)?(www\.)?(youtube\.com|youtu\.be)/\S+"

def link_youtube_handler(bot):
    @bot.message_handler(func=lambda message: re.search(YOUTUBE_REGEX, message.text))
    def handle_youtube_link(message):
        try:
            log.info('usuario esta tentando fazer download')
            print('usuario esta tentando fazer um download')
            
            chat_id = message.chat.id
            
            youtube_link = message.text.strip()
            titulo = sanitize_filename(get_title(youtube_link))
            thumb = get_thumb(youtube_link)
            
            bot.user_data[chat_id] = {
                'link': youtube_link,
                'title': titulo,
                'filename': f'{titulo}.m4a'
            }
            
            print(f'{titulo}: {youtube_link}')
            log.info(f'{titulo}: {youtube_link}')
            
            markup = InlineKeyboardMarkup()
            markup.add(
            InlineKeyboardButton("Video", callback_data="option_video"),
            InlineKeyboardButton("Audio", callback_data="option_audio"),
            InlineKeyboardButton("Cancel", callback_data="option_cancel")
            )
            
            message = bot.send_photo(chat_id, thumb, f'<b>{titulo}</b>\n\n<b>Escolha uma opção</b>', reply_markup=markup, parse_mode='HTML')
            
        except Exception as e:
            log.error(e)
            bot.send_message(message.chat.id, "O Download falhou, tente novamente...")