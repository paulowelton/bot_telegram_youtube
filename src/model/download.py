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

def download_video(link, filename):
    yt = YouTube(link)
    
    login = os.getlogin()
    path_video = f'C:\\Users\\{login}\\Desktop\\bot_telegram_youtube\\video\\'
    
    stream = yt.streams.filter(progressive=True, file_extension="mp4", res="360p").first()
    cam = stream.download(output_path=f'{path_video}', filename=filename)
    
    print(f'caminho: {cam}')
    log.info(f'caminho: {cam}')
    
    return cam


def download_audio(link, filename):
    
    try:
        log.info('baixando audio...')
        print('baixando audio...')
        
        yt = YouTube(link)
        
        login = os.getlogin()
        path_audio = f'C:\\Users\\{login}\\Desktop\\bot_telegram_youtube\\audio\\'
        
        ys = yt.streams.get_audio_only()
        cam = ys.download(output_path=path_audio, filename=filename)
        
        print(f'caminho: {cam}')
        log.info(f'caminho: {cam}')
        
        return cam
        
    
    except Exception as e:
        
        log.error(f'erro ao baixar video: {e}')
        print(f'erro ao baixar video: {e}')
        
        return False    
if __name__ == '__main__':
    download_video('', 'teste')