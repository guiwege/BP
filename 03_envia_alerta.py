###################################################################
# Verifica se os ultimos registros buscados na Hacker News
# devem alertar por terem a palavra chave
# Autor: Guilherme Wege Chagas
###################################################################

from datetime import datetime
from contextlib import closing
import smtplib
from email.message import EmailMessage
import sqlite3
import os


def printLog(*args):
    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ':', *args)

printLog('Iniciando script:', os.path.basename(__file__))

def send_alert(ids):
    guser = "guilhermewc@gmail.com"
    gpass = "Gwcc43976119!!"

    try:        
        msg = EmailMessage()
        msg.set_content('Os seguintes Ids contém a palavra chave procurada:\n' + ', '.join(str(id) for id in ids))
        msg['Subject'] = 'Hacker News - Palavra chave encontrada!'
        msg['From'] = guser
        msg['To'] = guser

        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(guser, gpass)
        #server.sendmail(guser, guser, msg)
        server.send_message(msg)
        server.close()
    except Exception as e:
        printLog('ERRO: Não foi possível enviar o alerta:', str(e))


with sqlite3.connect('banco.db') as con:
    with closing(con.cursor()) as cur:
        try:
            dt_carga = datetime.now().strftime('%Y-%m-%d')
            # Verifica se a palavra chave está em algum dos registros novos e envia alerta
            # Aqui é possível resolver mais de uma maneira, como:
            # - Verificar direto na stage se a palavra chave "chegou" (Estou usando este método)
            # - Olhar todos os registros da target onde dt_carga = max(dt_carga), ou seja, pegar o
            # ultimo movimento, e verificar se algum deles possui a palavra chave

            ids = []
            #for row in cur.execute(r'SELECT DISTINCT comment_id FROM comments where dt_carga = ?-- and text like "%linux%";', [dt_carga]):
            for row in cur.execute(r'SELECT DISTINCT comment_id FROM stg_comments where text like "%linux%";'):
                ids.append(int(row[0]))

            if ids:
                # Deixei um simples print aqui apenas para exemplificar o alerta.
                # Já trabalhei com o envio de e-mails via python (Normalmente para mim mesmo), 
                # mas sei que é possível utilizar notificações push, apis, etc. Para notificar.
                printLog('Enviando alerta com os ids encontrados:', ids)
                send_alert(ids)
                printLog('OK')
                #envia_email_alerta()
            else:
                printLog('Não existem alertas para enviar neste movimento.')
        
            printLog(f'Script {os.path.basename(__file__)} finalizou com sucesso')
        except Exception as e:
            printLog('ERRO:', str(e))
            printLog(f'Script {os.path.basename(__file__)} finalizou com erro')
            os.sys.exit(1)


