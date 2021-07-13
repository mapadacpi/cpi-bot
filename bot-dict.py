##
#   CPI Covid-19
#   Ferramenta que gera o dicionário geral dos documentos de forma automática,
#   utilizando os outros módulos desse repositório.
##

## CLI

import argparse

parser = argparse.ArgumentParser(description='CPI Covid-19: Bot de Dicionário')
parser.add_argument('-s', metavar='START', type=int, nargs=1, default=[1],
                    help='Primeiro documento')
parser.add_argument('-e', metavar='END', type=int, nargs=1, default=[9999],
                    help='Último documento')
parser.add_argument('--batch', metavar='BATCH', type=int, nargs=1, default=5,
                    help='Quantidade de documentos a processar por batch')

args = parser.parse_args()
START = args.s[0]
END = args.e[0]
BATCH = args.batch

##

import os
import json

# Usa o `scrape` para atualizar a lista de documentos em `json/docs.json`
os.system('python scrape.py')

# Carrega a lista de documentos do arquivo `json/docs.json`
docs = []
with open('json/docs.json') as file:
    docs = json.load(file)

# Confere se o arquivo "dict.json" já existe, e carrega seus dados
dict = {}
if (os.path.isfile('json/dict.json')):
    with open('json/dict.json') as file:
        dict = json.load(file)

def run(start, end):
    # Baixa os arquivos
    os.system('python download.py --pdf -s ' + str(start) + ' -e ' + str(end))

    # Extrai o texto dos arquivos um por um
    # Isso é feito para continuar rodando caso algum OCR falhe (em arquivos muito grandes)
    for e in range(start, end+1):
        result = os.system('python extract.py -s ' + str(e) + ' -e ' + str(e))
        # Extração de texto falhou. Cria um arquivo vazio para evitar de rodar novamente
        if (result != 0):
            print("! Falha na extração. Conferir manualmente !")

    # Gera o dicionário de cada arquivo
    os.system('python dict.py -s ' + str(start) + ' -e ' + str(end))

    # Apaga os arquivos originais em PDF (muito pesados)
    print("Excluindo arquivos originais...")
    for e in range(start-1, end):
        for link in docs[e]['links']:
            path = 'pdf/'+docs[e]['id']+'_'+(link[0]).replace('/','#')+'.pdf'
            print('\t'+path)
            if (os.path.isfile(path)):
                os.remove(path)

for start in range(START, END, BATCH):
    print("## BATCH " + str(start) + "~" + str(start+BATCH-1) + " ##")
    run(start, start+BATCH-1)
