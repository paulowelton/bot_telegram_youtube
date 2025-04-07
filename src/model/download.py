import logging as log
import os
from pytubefix import YouTube
from pytubefix.cli import on_progress

def get_thumb(link):
    yt = YouTube(link, on_progress_callback=on_progress)
    
    thumb = yt.thumbnail_url
    
    return thumb


def get_title(link):
    yt = YouTube(link, on_progress_callback=on_progress)
    
    titulo = yt.title
    
    return titulo

def download_video(link, titulo):
    yt = YouTube(link)
    
    login = os.getlogin()
    path_audio = f'C:\\Users\\{login}\\Desktop\\bot_telegram_yt\\video\\'
    stream = yt.streams.get_lowest_resolution()
    stream.download(output_path=f'{path_audio}', filename=f'{titulo}.mp4')
    
    print('download concluido')


def download_audio(link, filename):
    
    try:
        print(f'link recebido pra download: {link}')
        
        log.info('baixando audio...')
        
        yt = YouTube(link)
        
        login = os.getlogin()
        path_audio = f'C:\\Users\\{login}\\Desktop\\bot_telegram_youtube\\audio\\'
        
        ys = yt.streams.get_audio_only()
        cam = ys.download(output_path=path_audio, filename=filename)
        
        print(f'caminho: {cam}')
        
        return cam
        
    
    except Exception as e:
        
        log.error(f'erro ao baixar video: {e}')
        
        return False    
if __name__ == '__main__':
    download_video('https://www.youtube.com/watch?v=3-qwqrQXsXQ&list=RD3-qwqrQXsXQ&start_radio=1', 'teste')