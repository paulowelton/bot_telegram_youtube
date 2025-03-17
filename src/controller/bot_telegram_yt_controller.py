import logging as log

from src.model.bot import bot

log.basicConfig(filename=f'log.txt', level=log.INFO, format=' %(asctime)s - %(levelname)s - %(message)s',datefmt='%d/%m/%Y %I:%M:%S %p')

try:
    log.info('BOT TELEGRAM YOUTUBE\n')
    
    print('starting bot')
    
    bot()
    
except Exception as e:
    
    log.error(f'Error: {e}')
    
finally:
    log.info('tarefa finalizada\n')