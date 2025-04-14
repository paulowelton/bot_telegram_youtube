def command_handlers(bot):
    @bot.message_handler(commands=['start', 'hello'])
    def send_instructions(message):
        bot.reply_to(message, "Olá eu sou um Bot de Download\n\nMe envie um link do Youtube")