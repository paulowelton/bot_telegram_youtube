import logging as log
import time
import telebot
import re
from src.model.download import download_audio
from src.model.download import download_video
from src.model.apagar_arquivos import apagar_arquivos
from src.model.download import get_title
from src.model.download import get_thumb
from src.model.enviar_email import enviar_email
from src.model.upload_file import upload_to_pixeldrain
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

BOT_TOKEN = '8008948209:AAGcIJmEhB81t-oKNJsljyG_4brDM5y8Ifk'

YOUTUBE_REGEX = r"(https?://)?(www\.)?(youtube\.com|youtu\.be)/\S+"

def sanitize_filename(filename):
    return re.sub(r'[^a-zA-Z0-9_-]', '_', filename)

def bot():
    print('bot chamado')
    log.info('bot chamado')
    
    bot = telebot.TeleBot(BOT_TOKEN)
    
    bot.remove_webhook()
    time.sleep(1)
    
    user_data = {}
    
    @bot.message_handler(commands=['start', 'hello'])
    def send_instructions(message):
        bot.reply_to(message, "Olá eu sou um Bot de Download\n\nMe envie um link do Youtube")
    
    def processar_escolha(message, dados):
        escolha = message.text.strip()
        chat_id = message.chat.id
        
        link = dados['link']
        filename = dados['filename']
        
        if escolha not in ['1','2']:
            bot.send_message(chat_id, 'Opção Indisponivel')
            return    
        
        if escolha == '1':
            msg = bot.send_message(chat_id, 'Digite seu endereço de E-mail: ')
            
            bot.register_next_step_handler(msg, enviar_video_via_email, user_data[chat_id])
        if escolha == '2':
            caminho = download_video(link, filename)
            
            link_download = upload_to_pixeldrain(caminho)
            
            bot.send_message(chat_id, f'Link para donwnload: <a href="{link_download}">Clique Aqui</a>\n\nPrazo de 60 dias para download', parse_mode='HTML')
            
            apagar_arquivos(caminho)
            
            # limpar dados
            user_data.pop(chat_id, None)    
        
    def enviar_video_via_email(message, dados):
        email = message.text.strip()
        chat_id = message.chat.id
        
        link = dados['link']
        filename = dados['filename']
        
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            bot.send_message(chat_id, "Email inválido. Por favor, tente novamente:")
            return
        
        caminho = download_video(link, filename)
        
        try:
            enviar_email(email, caminho, filename)
            
            bot.send_message(chat_id, 'Video enviado com sucesso')
        except:
            bot.send_message(chat_id, f'Erro ao enviar email para: {email}')
            
        
        apagar_arquivos(caminho)
        
        
    @bot.callback_query_handler(func=lambda call: True)
    def callback_query(call):
        chat_id = call.message.chat.id
        message_id = call.message.message_id
        
        try:
            if chat_id not in user_data:
                bot.answer_callback_query(call.id, 'Sessão expirada!')
                return
            
            data = user_data[chat_id]
            link = data['link']
            titulo = data['title']
            filename = data['filename']
            
            if call.data == "option_audio":
                print('usuario pediu a opcao audio')
                log.info('usuario pediu a opcao audio')
                bot.send_message(chat_id, 'Aguardando Download...')
                
                caminho = download_audio(link, filename)
                
                with open(caminho, "rb") as audio:
                    bot.send_audio(chat_id, audio, caption=f"<b>{titulo}</b>\n\n<b>Criador: </b><a href='https://github.com/paulowelton'>GitHub</a>", parse_mode='HTML', timeout=120)
                apagar_arquivos(caminho)
                
                print('audio enviado\n')
                log.info('audio enviado\n')
                                                                                                                                         
            if call.data == "option_video":
                print('o usuario pediu a opcao video')
                log.info('o usuario pediu a opcao video')                
                
                bot.send_message(chat_id, '<b>Escolha por onde você quer receber o video:</b>\n<b>1 - Email</b> (Limite de 25mb)\n<b>2 - Link de Download</b> (Limite de 1GB)', parse_mode='HTML')
                
                bot.register_next_step_handler(call.message, processar_escolha ,user_data[chat_id])
                                
            if call.data == "option_cancel":
                print('usuario cancelou o download')
                log.info('usuario cancelou o download')
                
                bot.delete_message(chat_id, message_id)
                bot.send_message(chat_id, 'Canceled')
            
            # deleta as mesagens
            try:
                bot.delete_message(chat_id, message_id)
            except:
                print('mensagem não deletada')
                log.info('mensagem não deletada')
         
        except Exception as e:
            log.info(e)
            print(e)
            
            bot.send_message(call.message.chat.id, "Ocorreu um erro ao processar sua escolha.")
    
    @bot.message_handler(func=lambda message: re.search(YOUTUBE_REGEX, message.text))
    def handle_youtube_link(message):
        try:
            log.info('usuario esta tentando fazer download')
            print('usuario esta tentando fazer um download')
            
            chat_id = message.chat.id
            
            youtube_link = message.text.strip()
            titulo = sanitize_filename(get_title(youtube_link))
            thumb = get_thumb(youtube_link)
            
            user_data[chat_id] = {
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
            
    bot.infinity_polling(timeout=120, long_polling_timeout=120)

if __name__ == '__main__':
    bot()