import os

def apagar_arquivos(caminho):
    try:
        os.unlink(caminho)
    except:
        pass