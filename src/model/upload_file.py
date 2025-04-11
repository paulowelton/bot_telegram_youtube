import requests

def upload_to_pixeldrain(file_path):
    with open(file_path, 'rb') as f:
        files = {'file': f}
        # Autenticação básica: username vazio, API key como senha
        response = requests.post(
            'https://pixeldrain.com/api/file',
            files=files,
            auth=('', '11cc5500-5a7e-44b2-a225-b4d5e941a029')
        )

        if response.status_code in [200,201]:
            file_id = response.json()['id']
            return f'https://pixeldrain.com/u/{file_id}'
        else:
            print("Erro:", response.text)
            return None

if __name__ == '__main__':
    api_key = '11cc5500-5a7e-44b2-a225-b4d5e941a029'
    link = upload_to_pixeldrain("C:\\Users\\paulo.welton\\Desktop\\bot_telegram_youtube\\video\\teste.XLS", api_key)
    print("Link do arquivo:", link)
