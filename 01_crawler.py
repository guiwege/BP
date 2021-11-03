###################################################################
# Busca comentários no Hacker News e carrega na stage
# Autor: Guilherme Wege Chagas
###################################################################

# Busca o id do post mais recente para começar a analisar
from datetime import datetime
from contextlib import closing
from random import randint
import urllib.request
import json
import sqlite3
import os

def printLog(*args):
    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ':', *args)

# Busca o maior ID existente no Hacker News
def get_most_recent_hn_id():
    with urllib.request.urlopen('https://hacker-news.firebaseio.com/v0/maxitem.json') as urlin:
        data = json.loads(urlin.read().decode())
        #printLog(data)
        return int(data)

# Busca o maior ID existente na tabela comments
def get_last_processed_id():
    with sqlite3.connect('banco.db') as con:
        with closing(con.cursor()) as cur:
            for row in cur.execute('SELECT coalesce(max(comment_id), 0) from comments;'):
                last_id = int(row[0])
                return last_id
    
printLog('Iniciando script:', os.path.basename(__file__))

most_recent_hn_id = get_most_recent_hn_id()
last_processed_id = get_last_processed_id()

printLog('Maior id existente no Hacker News:', most_recent_hn_id)
printLog('Maior id existente na tabela comments:', last_processed_id)
#printLog(f'Ultimo id que foi processado na target: {last_processed_id}')

# Começa a processar do mais novo para o mais antigo, e vai inserindo na stage 
with sqlite3.connect('banco.db') as con:
    with closing(con.cursor()) as cur:
        try:
            # Limpa a stage antes de começar
            printLog('Limpa a stage')
            cur.execute('DELETE from stg_comments;')
            printLog('OK')

            printLog(f"Iniciando processamento do id: {last_processed_id+1}, até o: {most_recent_hn_id}")

            # A variavel abaixo foi criada para ser possível "simular" um movimento diário
            # Aqui, estou definindo que cada dia teria entre 100~200 ids
            contador_simulação_de_movimento = randint(1000, 1000)
            printLog('Contador para simular um movimento:', contador_simulação_de_movimento)

            for n, id in enumerate(range(last_processed_id+1, most_recent_hn_id+1)):

                # Interrompe a execução para ser possível continuar da proxima
                # Sem ter que ler toda a base de uma só vez
                if n>contador_simulação_de_movimento:
                    break

                with urllib.request.urlopen(f'https://hacker-news.firebaseio.com/v0/item/{id}.json?print=pretty') as urlin:
                    data = json.loads(urlin.read().decode())

                    if not data['type']=='comment':
                        printLog(f'O id {id} não é um \'comment\', ignorando...')

                    # Se for comentario, prosseguir
                    else:
                        printLog(f'Lendo o id: {id}, e inserindo na stage...')
                        parent_id = data['parent']
                        user_name = data['by']
                        text = data['text']
                        time = data['time']
                        
                        print(data)
                        # Insere na stage
                        cur.execute(f"INSERT INTO stg_comments VALUES (?,?,?,?,?)", [id, user_name, parent_id, time, text])
                        printLog('OK')

            printLog(f'Script {os.path.basename(__file__)} finalizou com sucesso')
        except Exception as e:
            printLog('ERRO:', str(e))
            printLog(f'Script {os.path.basename(__file__)} finalizou com erro')
            os.sys.exit(1)





