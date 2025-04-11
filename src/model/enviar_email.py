import smtplib as smtp
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# Com o módulo smtplib, envie um e-mail para você mesmo (ou para alguém de sua escolha)
# com o relatório gerado. Utilize o módulo email para estruturar corretamente o e-mail.
def enviar_email(emailDestinatario, caminho, filename):
    try:
        print(f'enviando email para {emailDestinatario}')
        
        #*conectando no servidor do gmail
        smtpObj = smtp.SMTP('smtp.gmail.com', 587)
        conexao = smtpObj.ehlo()
        smtpObj.starttls()
        emailRemetente = 'pythonemail08@gmail.com'
        smtpObj.login(emailRemetente, 'nwwe ossa loxf shlp')


        msg = MIMEMultipart()
        msg['From'] = emailRemetente
        msg['To'] = emailDestinatario
        msg['Subject'] = f'{filename.upper()}'
        msg.attach(MIMEText(f'Envio do arquivo <b>{filename}</b> feito pelo bot via telegram', 'html'))

        attachment = open(caminho, 'rb')

        att = MIMEBase('application', 'octet-stream')
        att.set_payload(attachment.read())
        encoders.encode_base64(att)

        att.add_header('Content-Disposition', f'attachment; filename={filename}')
        attachment.close()
        msg.attach(att)

        smtpObj.sendmail(msg['From'], msg['To'], msg.as_string())

        print('email enviado com sucesso')

        smtpObj.quit()
        
    except Exception as e:
        print(f"ocorreu um erro: {e}")