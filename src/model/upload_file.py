import requests

def upload_transfer_sh(file_path):
    try:
        with open(file_path, 'rb') as f:
            file_name = file_path.split('/')[-1]
            response = requests.put(f'https://transfer.sh/{file_name}', data=f)
        
        if response.status_code == 200:
            print("Upload feito com sucesso!")
            print("Link:", response.text.strip())
            return response.text.strip()
        else:
            print("Erro ao enviar:", response.status_code, response.text)
            return None
    except Exception as e:
        print("Erro:", e)
        return None

def upload_to_anonfiles(file_path):
    url = 'https://api.anonfiles.com/upload'
    with open(file_path, 'rb') as f:
        files = {'file': (file_path, f)}
        response = requests.post(url, files=files)

    try:
        result = response.json()
        if result['status']:
            file_url = result['data']['file']['url']['full']
            print(f"Arquivo enviado com sucesso: {file_url}")
            return file_url
        else:
            print("Erro no upload:", result)
    except Exception as e:
        print("Erro ao tentar decodificar JSON:", e)

# Exemplo de uso
upload_to_anonfiles('C:\\Users\\paulo.welton\\Desktop\\bot_telegram_youtube\\video\\FIZ_UM_MALWARE.m4a')
