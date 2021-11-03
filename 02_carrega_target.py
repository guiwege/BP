###################################################################
# Lê da stage de comentários e carrega na target
# Autor: Guilherme Wege Chagas
###################################################################

# Busca o id do post mais recente para começar a analisar
from datetime import datetime
from contextlib import closing
import os
import sqlite3

def printLog(*args):
    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ':', *args)

printLog('Iniciando script:', os.path.basename(__file__))

# Lendo dados da stage e carregando na target
with sqlite3.connect('banco.db') as con:
    with closing(con.cursor()) as cur:
        try:
            dt_carga = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            # Deleta da target os registros que chegaram na stage (reprocessamento)
            printLog('Deleta da target os registros que chegaram na stage (reprocessamento)')
            cur.execute('DELETE FROM comments WHERE comment_id IN (select comment_id from stg_comments);')
            printLog('OK')


            # Insere na target
            printLog('Inserindo na target')
            cur.execute('''
            INSERT INTO comments 
            SELECT
                comment_id
                ,user_name
                ,parent_id
                ,DATETIME(time, 'unixepoch') as dt_comment
                ,? as dt_carga
                ,text
            FROM stg_comments;
            ''', [dt_carga])
            printLog('OK')

            printLog(f'Script {os.path.basename(__file__)} finalizou com sucesso')
        except Exception as e:
            printLog('ERRO:', str(e))
            printLog(f'Script {os.path.basename(__file__)} finalizou com erro')
            os.sys.exit(1)
